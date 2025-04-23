from contextlib import contextmanager
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator, Optional
from maleo_foundation.utils.logger import BaseLogger

class SessionManager:
    _logger:Optional[BaseLogger] = None
    _sessionmaker:Optional[sessionmaker[Session]] = None

    @classmethod
    def initialize(cls, logger:BaseLogger, engine:Engine) -> None:
        """Initialize the sessionmaker if not already initialized."""
        if cls._sessionmaker is None:
            cls._logger = logger
            cls._sessionmaker = sessionmaker(bind=engine, expire_on_commit=False)
            cls._logger.info("SessionManager initialized successfully.")

    @classmethod
    def _session_handler(cls) -> Generator[Session, None, None]:
        """Reusable function for managing database sessions."""
        if cls._logger is None:
            raise RuntimeError("Logger has not been initialized. Call initialize() first.")
        if cls._sessionmaker is None:
            raise RuntimeError("SessionLocal has not been initialized. Call initialize() first.")

        session = cls._sessionmaker()
        cls._logger.debug("New database session created.")
        try:
            yield session  #* Provide session
            session.commit()  #* Auto-commit on success
        except SQLAlchemyError as e:
            session.rollback()  #* Rollback on error
            cls._logger.error(f"[SQLAlchemyError] Database transaction failed: {e}", exc_info=True)
            raise
        except Exception as e:
            session.rollback()  #* Rollback on error
            cls._logger.error(f"[Exception] Database transaction failed: {e}", exc_info=True)
            raise
        finally:
            session.close()  #* Ensure session closes
            cls._logger.debug("Database session closed.")

    @classmethod
    def inject(cls) -> Generator[Session, None, None]:
        """Returns a generator that yields a SQLAlchemy session for dependency injection."""
        return cls._session_handler()

    @classmethod
    @contextmanager
    def get(cls) -> Generator[Session, None, None]:
        """Context manager for manual session handling. Supports `with SessionManager.get() as session:`"""
        yield from cls._session_handler()

    @classmethod
    def dispose(cls) -> None:
        """Dispose of the sessionmaker and release any resources."""
        if cls._sessionmaker is not None:
            cls._sessionmaker.close_all()
            cls._sessionmaker = None

        cls._logger.info("SessionManager disposed successfully.")
        cls._logger = None