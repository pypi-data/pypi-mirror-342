from sqlalchemy import Engine, MetaData, Column, Integer, UUID, TIMESTAMP, Enum, func
from sqlalchemy.orm import declarative_base, declared_attr
from uuid import uuid4
from maleo_foundation.enums import BaseEnums
from maleo_foundation.utils.formatter.case import CaseFormatter

class DatabaseManager:
    class BaseMixin:
        __abstract__ = True

        @declared_attr
        def __tablename__(cls) -> str:
            return CaseFormatter.to_snake_case(cls.__name__)

        #* ----- ----- Common columns definition ----- ----- *#

        #* Identifiers
        id = Column(Integer, primary_key=True)
        uuid = Column(UUID, default=uuid4, unique=True, nullable=False)

        #* Timestamps
        created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
        updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
        deleted_at = Column(TIMESTAMP(timezone=True))
        restored_at = Column(TIMESTAMP(timezone=True))
        deactivated_at = Column(TIMESTAMP(timezone=True))
        activated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

        #* Statuses
        status = Column(Enum(BaseEnums.StatusType, name="statustype"), default=BaseEnums.StatusType.ACTIVE, nullable=False)

    Base = declarative_base()  #* Correct way to define a declarative base

    #* Explicitly define the type of metadata
    metadata:MetaData = Base.metadata

    @classmethod
    def initialize(cls, engine:Engine):
        """Creates the database tables if they do not exist."""
        cls.metadata.create_all(engine)