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
from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import SqlAlchemyConfig
from archipy.helpers.metaclasses.singleton import Singleton


class SessionManagerAdapter(SessionManagerPort, metaclass=Singleton):
    """Manages SQLAlchemy database sessions for synchronous operations.

    This adapter creates and manages database sessions using SQLAlchemy's
    session management system. It implements the Singleton pattern to ensure
    a single instance exists throughout the application lifecycle.

    Args:
        orm_config (SqlAlchemyConfig, optional): Configuration for the ORM.
            If None, retrieves from global config. Defaults to None.

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.session_manager_adapters import SessionManagerAdapter
        >>> from archipy.configs.config_template import SqlAlchemyConfig
        >>>
        >>> # Using default global configuration
        >>> manager = SessionManagerAdapter()
        >>> session = manager.get_session()
        >>>
        >>> # Using custom configuration
        >>> custom_config = SqlAlchemyConfig(DATABASE="custom_db", HOST="localhost")
        >>> custom_manager = SessionManagerAdapter(custom_config)
    """

    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        """Initializes the session manager.

        Args:
            orm_config: Configuration for SQLAlchemy. If None, retrieves from global config.
        """
        configs = BaseConfig.global_config().SQLALCHEMY if orm_config is None else orm_config
        self.engine = self._create_engine(configs)
        self._session_generator = self._get_session_generator()

    @override
    def get_session(self) -> Session:
        """Retrieves a SQLAlchemy session from the session factory.

        The session is scoped to the current context to ensure thread safety.

        Returns:
            Session: A SQLAlchemy session instance that can be used for
                database operations.

        Examples:
            >>> session = session_manager.get_session()
            >>> user = session.query(User).filter_by(id=1).first()
        """
        return self._session_generator()  # type: ignore[no-any-return]

    @override
    def remove_session(self) -> None:
        """Removes the current session from the registry.

        This should be called when you're done with a session to prevent
        resource leaks, particularly at the end of web requests.

        Examples:
            >>> session = session_manager.get_session()
            >>> # Use session for operations
            >>> session_manager.remove_session()
        """
        self._session_generator.remove()

    def _get_session_generator(self) -> scoped_session:
        session_maker = sessionmaker(self.engine)
        return scoped_session(session_maker)

    @staticmethod
    def _create_engine(configs: SqlAlchemyConfig) -> Engine:
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
            pool_timeout=configs.POOL_TIMEOUT,
            pool_use_lifo=configs.POOL_USE_LIFO,
            query_cache_size=configs.QUERY_CACHE_SIZE,
            max_overflow=configs.POOL_MAX_OVERFLOW,
        )


class AsyncSessionManagerAdapter(AsyncSessionManagerPort, metaclass=Singleton):
    """Manages SQLAlchemy database sessions for asynchronous operations.

    This adapter creates and manages asynchronous database sessions using SQLAlchemy's
    async session management system. It implements the Singleton pattern to ensure
    a single instance exists throughout the application lifecycle.

    Args:
        orm_config (SqlAlchemyConfig, optional): Configuration for the ORM.
            If None, retrieves from global config. Defaults to None.

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.session_manager_adapters import AsyncSessionManagerAdapter
        >>> from archipy.configs.config_template import SqlAlchemyConfig
        >>>
        >>> # Using default global configuration
        >>> manager = AsyncSessionManagerAdapter()
        >>> session = manager.get_session()
        >>>
        >>> # Using custom configuration
        >>> custom_config = SqlAlchemyConfig(DATABASE="custom_db", HOST="localhost")
        >>> custom_manager = AsyncSessionManagerAdapter(custom_config)
    """

    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        """Initializes the async session manager.

        Args:
            orm_config: Configuration for SQLAlchemy. If None, retrieves from global config.
        """
        configs = BaseConfig.global_config().SQLALCHEMY if orm_config is None else orm_config
        self.engine = self._create_async_engine(configs)
        self._session_generator = self._get_session_generator()

    @override
    def get_session(self) -> AsyncSession:
        """Retrieves an async SQLAlchemy session from the session factory.

        The session is scoped to the current async task to ensure task safety.

        Returns:
            AsyncSession: An async SQLAlchemy session instance that can be used for
                database operations.

        Examples:
            >>> session = await session_manager.get_session()
            >>> user = await session.get(User, 1)
        """
        return self._session_generator()  # type: ignore[no-any-return]

    @override
    async def remove_session(self) -> None:
        """Removes the current async session from the registry.

        This should be called when you're done with a session to prevent
        resource leaks, particularly at the end of async web requests.

        Examples:
            >>> session = session_manager.get_session()
            >>> # Use session for operations
            >>> await session_manager.remove_session()
        """
        await self._session_generator.remove()

    def _get_session_generator(self) -> async_scoped_session:
        """Creates and returns a scoped session factory for async sessions.

        Returns:
            An async_scoped_session instance scoped to the current task.
        """
        session_maker: async_sessionmaker = async_sessionmaker(self.engine)
        return async_scoped_session(session_maker, current_task)

    @staticmethod
    def _create_async_engine(configs: SqlAlchemyConfig) -> AsyncEngine:
        """Creates an async SQLAlchemy engine from configuration.

        Args:
            configs: The SQLAlchemy configuration.

        Returns:
            An AsyncEngine instance configured according to the provided config.
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
            pool_size=configs.POOL_SIZE,
            pool_recycle=configs.POOL_RECYCLE_SECONDS,
            pool_reset_on_return=configs.POOL_RESET_ON_RETURN,
            pool_timeout=configs.POOL_TIMEOUT,
            pool_use_lifo=configs.POOL_USE_LIFO,
            query_cache_size=configs.QUERY_CACHE_SIZE,
            max_overflow=configs.POOL_MAX_OVERFLOW,
        )
