from typing import Dict
from typing import Optional

from imbue_core.computing_environment.computing_environment import ComputingEnvironment
from imbue_core.computing_environment.computing_environment import get_git_folder_paths
from imbue_core.computing_environment.computing_environment import get_head_hash
from imbue_core.computing_environment.computing_environment import get_modified_file_contents_by_path
from imbue_core.computing_environment.computing_environment import get_unmerged_and_staged_blob_contents_by_hash
from imbue_core.computing_environment.computing_environment import is_repo_conflicted
from imbue_core.frozen_utils import FrozenDict
from imbue_core.repo_state import ConflictType
from imbue_core.repo_state import ConflictedRepoOperation
from imbue_core.repo_state import GIT_FILE_PATH_NAMES_BY_CONFLICT_TYPE
from imbue_core.repo_state import RepoState


async def get_special_git_file_contents_by_path_for_conflict_type(
    computing_environment: ComputingEnvironment, conflict_type: ConflictType
) -> Dict[str, bytes]:
    filenames = GIT_FILE_PATH_NAMES_BY_CONFLICT_TYPE[conflict_type]
    git_file_contents_by_path: Dict[str, bytes] = {}
    for filename in filenames:
        content = await computing_environment.read_file(f".git/{filename}", mode="rb")
        assert isinstance(content, bytes), f"Expected bytes, got {type(content)}"
        git_file_contents_by_path[filename] = content
    return git_file_contents_by_path


async def get_conflict_type_from_computing_environment(
    computing_environment: ComputingEnvironment,
) -> Optional[ConflictType]:
    if await is_repo_conflicted(computing_environment):
        files = await get_git_folder_paths(computing_environment)
        if "MERGE_HEAD" in files:
            return ConflictType.MERGE
        # elif "REBASE_HEAD" in files:
        #     return ConflictType.REBASE
        # elif "CHERRY_PICK_HEAD" in files:
        #     return ConflictType.CHERRY_PICK
        else:
            return ConflictType.APPLY
    else:
        return None


async def get_conflicted_repo_state_from_computing_environment(
    computing_environment: ComputingEnvironment,
) -> RepoState:
    index_content = await computing_environment.read_file(".git/index", mode="rb")
    assert isinstance(index_content, bytes)
    conflict_type = await get_conflict_type_from_computing_environment(computing_environment)
    assert conflict_type is not None
    special_git_file_contents_by_path = await get_special_git_file_contents_by_path_for_conflict_type(
        computing_environment, conflict_type
    )
    return RepoState(
        git_hash=await get_head_hash(computing_environment),
        repo_operation=ConflictedRepoOperation(
            conflict_type=conflict_type,
            modified_file_contents_by_path=FrozenDict(await get_modified_file_contents_by_path(computing_environment)),
            special_git_file_contents_by_path=FrozenDict(special_git_file_contents_by_path),
            index_content=index_content,
            blob_content_by_hash=FrozenDict(
                await get_unmerged_and_staged_blob_contents_by_hash(computing_environment)
            ),
        ),
    )
