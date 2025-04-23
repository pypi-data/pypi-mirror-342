from functools import cache

from sqlalchemy import create_engine

import momake.runlog.tables
from momake.runlog.db import metadata

FILE_URL = "momake.db"
URL = f"sqlite:///{FILE_URL}"


@cache
def engine():
    engine = create_engine(URL)
    metadata.create_all(engine, checkfirst=True)
    return engine
