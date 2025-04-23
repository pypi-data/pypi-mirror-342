from datetime import datetime
from datetime import timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from momake.runlog.conn import engine
from momake.runlog.tables import TaskTable


def get_last_task_run(task_id) -> Optional[datetime]:
    stmt = select(TaskTable.runtime).filter(
        TaskTable.task_id == task_id,
        TaskTable.runtime.isnot(None),
    ).order_by(TaskTable.runtime.desc())
    with Session(engine()) as db:
        result = db.execute(stmt).first()
        if result:
            return result.runtime.replace(tzinfo=timezone.utc)
    return None


def get_task(task_id: str, run_id: UUID) -> Optional[dict]:
    stmt = select(TaskTable).filter(
        TaskTable.task_id == task_id, TaskTable.run_id == run_id
    )
    with Session(engine()) as db:
        result = db.execute(stmt).first()
        if result:
            return result._asdict()
    return None
