from datetime import datetime

import attr


def _validate_git_timestamp(instance, attribute, value: str) -> None:
    try:
        datetime.fromisoformat(value)
    except ValueError:
        raise ValueError(f"Invalid git timestamp: {value}")


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class CommitTimestamp:
    author_ts: str = attr.ib(validator=_validate_git_timestamp)
    committer_ts: str = attr.ib(validator=_validate_git_timestamp)


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class CommitMetadata:
    commit: str
    tree_hash: str
    message: str
    commit_time: CommitTimestamp

    @property
    def body(self) -> str:
        return self.message.split("\n", 1)[-1]

    @property
    def subject(self) -> str:
        return self.message.split("\n", 1)[0]
