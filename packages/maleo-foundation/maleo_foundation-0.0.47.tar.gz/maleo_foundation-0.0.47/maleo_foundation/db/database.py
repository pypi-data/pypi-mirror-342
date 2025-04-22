from sqlalchemy import Engine, MetaData, Column, Integer, UUID, TIMESTAMP, Enum, func
from sqlalchemy.orm import declarative_base, declared_attr
from uuid import uuid4
from maleo_foundation.enums import BaseEnums
from maleo_foundation.utils.formatter.case import CaseFormatter

Base = declarative_base()  #* Correct way to define a declarative base

class DatabaseManager:
    class Base(Base):  #* Inheriting from declarative_base
        __abstract__ = True  #* Ensures this class is not treated as a table itself

        @declared_attr
        def __tablename__(cls) -> str:
            """Automatically generates table name (in snake_case) based on class name."""
            return CaseFormatter.to_snake_case(cls.__name__)

        #* ----- ----- Common columns definition ----- ----- *#

        #* Identifiers
        id = Column(name="id", type_=Integer, primary_key=True)
        uuid = Column(name="uuid", type_=UUID, default=uuid4, unique=True, nullable=False)

        #* Timestamps
        created_at = Column(name="created_at", type_=TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
        updated_at = Column(name="updated_at", type_=TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
        deleted_at = Column(name="deleted_at", type_=TIMESTAMP(timezone=True))
        restored_at = Column(name="restored_at", type_=TIMESTAMP(timezone=True))
        deactivated_at = Column(name="deactivated_at", type_=TIMESTAMP(timezone=True))
        activated_at = Column(name="activated_at", type_=TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

        #* Statuses
        status = Column(name="status", type_=Enum(BaseEnums.StatusType, name="statustype"), default=BaseEnums.StatusType.ACTIVE, nullable=False)

    #* Explicitly define the type of metadata
    metadata:MetaData = Base.metadata

    @staticmethod
    def initialize(engine: Engine):
        """Creates the database tables if they do not exist."""
        DatabaseManager.metadata.create_all(engine)
