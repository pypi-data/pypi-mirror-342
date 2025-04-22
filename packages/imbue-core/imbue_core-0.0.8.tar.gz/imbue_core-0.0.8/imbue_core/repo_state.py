from enum import StrEnum
from typing import Dict
from typing import Self
from typing import Tuple

import attr

from imbue_core.cattrs_serialization import cached_serializable_property
from imbue_core.cattrs_serialization import serializable_property
from imbue_core.frozen_utils import FrozenDict
from imbue_core.serialization_types import Serializable

ResourceURL = str


class ConflictType(StrEnum):
    MERGE = "MERGE"
    REBASE = "REBASE"
    CHERRY_PICK = "CHERRY_PICK"
    APPLY = "APPLY"
    REVERT = "REVERT"
    BISECT = "BISECT"


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class RepoOperation(Serializable):
    pass

    @serializable_property
    def is_empty(self) -> bool:
        """Whether this repo operation leaves the repo unchanged.

        Defaults to False. But should be overridden by subclasses as appropriate.
        """
        return False


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class ConflictedRepoOperation(RepoOperation):
    blob_content_by_hash: FrozenDict[str, bytes]
    index_content: bytes
    modified_file_contents_by_path: FrozenDict[str, bytes]
    conflict_type: ConflictType
    special_git_file_contents_by_path: FrozenDict[str, bytes]


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class CleanRepoOperation(RepoOperation):
    """
    A clean repo operation is a repo operation that has no conflicts.

    It is a contains the staged diff, the unstaged diff, and the combination of the previous two.
    """

    def __attrs_post_init__(self) -> None:
        if self.combined_diff.strip() != "":
            assert (
                self.staged_diff.strip() != "" or self.unstaged_diff.strip() != ""
            ), "combined diff is not empty, so staged and unstaged diffs must be non-empty"

    combined_diff: str
    staged_diff: str = ""
    unstaged_diff: str = ""

    @serializable_property
    def is_empty(self) -> bool:
        return self.combined_diff.strip() == ""


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class RepoState(Serializable):
    git_hash: str
    repo_operation: CleanRepoOperation | ConflictedRepoOperation

    @serializable_property
    def is_conflicted(self) -> bool:
        return isinstance(self.repo_operation, ConflictedRepoOperation)

    @serializable_property
    def has_operations(self) -> bool:
        return (
            isinstance(self.repo_operation, ConflictedRepoOperation) or self.repo_operation.combined_diff.strip() != ""
        )

    @cached_serializable_property
    def type_name(self) -> str:
        return self.__class__.__name__

    def build_with_new_commit(self, git_hash: str) -> Self:
        return attr.evolve(self, git_hash=git_hash)


GIT_FILE_PATH_NAMES_BY_CONFLICT_TYPE: Dict[ConflictType, Tuple[str, ...]] = {
    ConflictType.MERGE: ("MERGE_HEAD", "AUTO_MERGE", "MERGE_MSG", "MERGE_MODE"),
    ConflictType.REBASE: ("REBASE_HEAD",),
    ConflictType.CHERRY_PICK: ("CHERRY_PICK_HEAD",),
    ConflictType.APPLY: (),
    ConflictType.REVERT: ("REVERT_HEAD",),
}


def get_conflict_type_from_special_git_file_contents_by_path(
    special_git_file_contents_by_path: Dict[str, bytes]
) -> ConflictType:
    if "MERGE_HEAD" in special_git_file_contents_by_path:
        return ConflictType.MERGE
    # elif "REBASE_HEAD" in special_git_file_contents_by_path:
    #     return ConflictType.REBASE
    # elif "CHERRY_PICK_HEAD" in special_git_file_contents_by_path:
    #     return ConflictType.CHERRY_PICK
    else:
        return ConflictType.APPLY
