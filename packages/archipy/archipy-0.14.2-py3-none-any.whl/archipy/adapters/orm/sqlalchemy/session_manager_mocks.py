from asyncio import current_task
from typing import override

from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from archipy.adapters.orm.sqlalchemy.session_manager_ports import AsyncSessionManagerPort, SessionManagerPort
from archipy.configs.config_template import SqlAlchemyConfig
from archipy.helpers.metaclasses.singleton import Singleton


class SessionManagerMock(SessionManagerPort, metaclass=Singleton):
    """Mock implementation of the SQLAlchemy session manager for testing.

    This class provides session management for in-memory SQLite databases,
    making it ideal for unit testing database operations without requiring
    a real database connection.

    Args:
        orm_config (SqlAlchemyConfig, optional): Custom SQLAlchemy configuration.
            If None, uses an in-memory SQLite database. Defaults to None.

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.session_manager_mocks import SessionManagerMock
        >>>
        >>> # Create a session manager with default in-memory SQLite
        >>> session_manager = SessionManagerMock()
        >>> session = session_manager.get_session()
        >>>
        >>> # Use session for database operations
        >>> session.add(User(name="Test User"))
        >>> session.commit()
        >>>
        >>> # Clean up when done
        >>> session_manager.remove_session()
    """

    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        """Initializes the session manager mock.

        Args:
            orm_config: Custom SQLAlchemy configuration. If None, uses an
                in-memory SQLite database with appropriate settings.
        """
        if orm_config:
            configs: SqlAlchemyConfig = orm_config
        else:
            configs: SqlAlchemyConfig = SqlAlchemyConfig(
                DRIVER_NAME="sqlite",
                DATABASE=":memory:",
                ISOLATION_LEVEL=None,
                PORT=None,
            )
        self.engine = self._create_engine(configs)
        self._session_generator = self._get_session_generator(configs)

    @override
    def get_session(self) -> Session:
        """Retrieves a SQLAlchemy session from the mock session factory.

        Returns:
            Session: A SQLAlchemy session instance that can be used for
                database operations on the in-memory database.
        """
        return self._session_generator()

    @override
    def remove_session(self) -> None:
        """Removes the current session from the registry.

        This should be called when you're done with a session to prevent
        resource leaks in testing environments.
        """
        self._session_generator.remove()

    def _get_session_generator(self, _: SqlAlchemyConfig) -> scoped_session:
        """Creates and returns a scoped session factory.

        Args:
            configs: The SQLAlchemy configuration.

        Returns:
            A scoped_session instance for the in-memory database.
        """
        session_maker = sessionmaker(self.engine)
        return scoped_session(session_maker)

    @staticmethod
    def _create_engine(configs: SqlAlchemyConfig) -> Engine:
        """Creates a SQLAlchemy engine for the in-memory database.

        Args:
            configs: The SQLAlchemy configuration.

        Returns:
            An Engine instance configured for the in-memory database.
        """
        url = URL.create(
            drivername=configs.DRIVER_NAME,
            username=configs.USERNAME,
            password=configs.PASSWORD,
            host=configs.HOST,
            port=configs.PORT,
            database=configs.DATABASE,
        )
        return create_engine(
            url,
            isolation_level=configs.ISOLATION_LEVEL,
            echo=configs.ECHO,
            echo_pool=configs.ECHO_POOL,
            enable_from_linting=configs.ENABLE_FROM_LINTING,
            hide_parameters=configs.HIDE_PARAMETERS,
            pool_pre_ping=configs.POOL_PRE_PING,
            pool_size=configs.POOL_SIZE,
            pool_recycle=configs.POOL_RECYCLE_SECONDS,
            pool_reset_on_return=configs.POOL_RESET_ON_RETURN,
            query_cache_size=configs.QUERY_CACHE_SIZE,
            connect_args={"check_same_thread": False},
        )


class AsyncSessionManagerMock(AsyncSessionManagerPort, metaclass=Singleton):
    """Asynchronous mock implementation of the SQLAlchemy session manager for testing.

    This class provides asynchronous session management for in-memory SQLite databases,
    making it ideal for unit testing asynchronous database operations without requiring
    a real database connection.

    Args:
        orm_config (SqlAlchemyConfig, optional): Custom SQLAlchemy configuration.
            If None, uses an in-memory SQLite database with aiosqlite. Defaults to None.

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.session_manager_mocks import AsyncSessionManagerMock
        >>>
        >>> # Create an async session manager with default in-memory SQLite
        >>> session_manager = AsyncSessionManagerMock()
        >>>
        >>> # Example async function using the mock session manager
        >>> async def test_database_operations():
        ...     session = session_manager.get_session()
        ...     # Use session for database operations
        ...     session.add(User(name="Test User"))
        ...     await session.commit()
        ...     # Clean up when done
        ...     await session_manager.remove_session()
    """

    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        """Initializes the async session manager mock.

        Args:
            orm_config: Custom SQLAlchemy configuration. If None, uses an
                in-memory SQLite database with aiosqlite driver and appropriate settings.
        """
        if orm_config:
            configs: SqlAlchemyConfig = orm_config
        else:
            configs: SqlAlchemyConfig = SqlAlchemyConfig(
                DRIVER_NAME="sqlite+aiosqlite",
                DATABASE=":memory:",
                ISOLATION_LEVEL=None,
                PORT=None,
            )
        self.engine = self._create_async_engine(configs)
        self._session_generator = self._get_session_generator(configs)

    @override
    def get_session(self) -> AsyncSession:
        """Retrieves an async SQLAlchemy session from the mock session factory.

        Returns:
            AsyncSession: An async SQLAlchemy session instance that can be used for
                asynchronous database operations on the in-memory database.
        """
        return self._session_generator()

    @override
    async def remove_session(self) -> None:
        """Removes the current async session from the registry.

        This should be called when you're done with a session to prevent
        resource leaks in testing environments.
        """
        await self._session_generator.remove()

    def _get_session_generator(self, _: SqlAlchemyConfig) -> async_scoped_session:
        """Creates and returns a scoped session factory for async sessions.

        Args:
            configs: The SQLAlchemy configuration.

        Returns:
            An async_scoped_session instance scoped to the current task.
        """
        session_maker: async_sessionmaker = async_sessionmaker(self.engine)
        return async_scoped_session(session_maker, current_task)

    @staticmethod
    def _create_async_engine(configs: SqlAlchemyConfig) -> AsyncEngine:
        """Creates an async SQLAlchemy engine for the in-memory database.

        Args:
            configs: The SQLAlchemy configuration.

        Returns:
            An AsyncEngine instance configured for the in-memory database.
        """
        url = URL.create(
            drivername=configs.DRIVER_NAME,
            username=configs.USERNAME,
            password=configs.PASSWORD,
            host=configs.HOST,
            port=configs.PORT,
            database=configs.DATABASE,
        )
        return create_async_engine(
            url,
            isolation_level=configs.ISOLATION_LEVEL,
            echo=configs.ECHO,
            echo_pool=configs.ECHO_POOL,
            enable_from_linting=configs.ENABLE_FROM_LINTING,
            hide_parameters=configs.HIDE_PARAMETERS,
            pool_pre_ping=configs.POOL_PRE_PING,
            pool_recycle=configs.POOL_RECYCLE_SECONDS,
            pool_reset_on_return=configs.POOL_RESET_ON_RETURN,
            query_cache_size=configs.QUERY_CACHE_SIZE,
        )
