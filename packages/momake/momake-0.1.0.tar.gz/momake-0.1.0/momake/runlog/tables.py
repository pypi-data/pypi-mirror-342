from sqlalchemy import UUID
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

from momake.runlog.db import SqlTable


class TaskTable(SqlTable):
    __tablename__ = "tasks"

    task_id = Column(String)
    run_id = Column(UUID)
    check_runtime = Column(DateTime(timezone=True))
    runtime = Column(DateTime(timezone=True))
    runtime_finish = Column(DateTime(timezone=True))
