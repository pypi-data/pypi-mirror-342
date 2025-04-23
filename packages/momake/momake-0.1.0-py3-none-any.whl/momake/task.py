from datetime import datetime
from datetime import timezone
from typing import Optional
from uuid import UUID
from uuid import uuid4

from click import echo
from click import style

from momake.runlog.commands import set_task_log
from momake.runlog.queries import get_last_task_run


class Task:
    name = None
    dependecies = []

    @property
    def task_id(self):
        return self.__class__.__name__

    def should_run(self, last_runtime: Optional[datetime], run_id: UUID) -> bool:
        return self.run(run_id)

    def should_run_task(self, run_id: UUID):
        last_runtime = get_last_task_run(self.task_id)
        for dependency in self.dependecies:
            if dependency.should_run(last_runtime, run_id):
                return True
        return False

    def action(self):
        pass

    def run(self, run_id: Optional[UUID] = None):
        run_id = run_id or uuid4()
        echo(style(f"Checking {self.name}...", fg="bright_yellow"))
        runlog = {}
        runlog["check_runtime"] = datetime.now(timezone.utc)
        if self.should_run_task(run_id):
            runlog["runtime"] = datetime.now(timezone.utc)
            echo(style(f"Running {self.name}...", fg="green"))
            self.action()
            runlog["runtime_finish"] = datetime.now(timezone.utc)
            result = True
        else:
            result = False
        set_task_log(self.task_id, run_id, **runlog)
        return result
