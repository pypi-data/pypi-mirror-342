import os
from sqlalchemy import create_engine, Engine
from typing import Optional
from maleo_foundation.utils.logger import BaseLogger

class EngineManager:
    _logger:Optional[BaseLogger] = None
    _engine:Optional[Engine] = None

    @classmethod
    def initialize(cls, logger:BaseLogger, url:Optional[str] = None) -> Engine:
        """Initialize the engine if not already initialized."""
        if cls._engine is None:
            cls._logger = logger
            url = url or os.getenv("DB_CONNECTION_STRING")
            if url is None:
                raise ValueError("DB_CONNECTION_STRING environment variable must be set if url is not provided")
            cls._engine = create_engine(url=url, echo=False, pool_pre_ping=True, pool_recycle=3600)
            cls._logger.info("EngineManager initialized successfully.")
        return cls._engine

    @classmethod
    def get(cls) -> Engine:
        """Retrieve the engine, initializing it if necessary."""
        if cls._logger is None:
            raise RuntimeError("Logger has not been initialized. Call initialize(db_connection_string, logger) first.")
        if cls._engine is None:
            raise RuntimeError("Engine has not been initialized. Call initialize(db_connection_string, logger) first.")

        return cls._engine

    @classmethod
    def dispose(cls) -> None:
        """Dispose of the engine and release any resources."""
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None

        cls._logger.info("Engine disposed successfully.")
        cls._logger = None