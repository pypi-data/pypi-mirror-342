from datetime import datetime
from datetime import timezone
from functools import cache
from pathlib import Path
from typing import Optional
from uuid import UUID


class Dependency:
    def has_changed(self, last_runtime: datetime, run_id: UUID) -> bool:
        return False

    def should_run(self, last_runtime: Optional[datetime], run_id: UUID) -> bool:
        if not last_runtime:
            return True
        return self.has_changed(last_runtime, run_id)


class AlwaysDependency(Dependency):
    def has_changed(self, last_runtime: datetime, run_id: UUID) -> bool:
        return True


class FileDependency(Dependency):
    def __init__(self, path: str, pattern: str):
        super().__init__()
        self.path = path
        self.pattern = pattern

    @cache
    def file_mtimes(self) -> list[datetime]:
        mtimes = []
        pathobj = Path(self.path)
        for path in pathobj.rglob(self.pattern):
            modified = datetime.fromtimestamp(path.lstat().st_mtime, tz=timezone.utc)
            mtimes.append(modified)
        return mtimes

    def has_changed(self, last_runtime: datetime, run_id: UUID) -> bool:
        if not self.file_mtimes():
            return True
        return min(self.file_mtimes()) > last_runtime
