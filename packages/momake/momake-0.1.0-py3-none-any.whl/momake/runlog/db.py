from sqlalchemy import UUID
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import MetaData

metadata = MetaData()


class Base:
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    def _asdict(self):
        data = dict(self.__dict__)
        del data["_sa_instance_state"]
        return data


SqlTable = declarative_base(cls=Base, metadata=metadata)
