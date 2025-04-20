from archipy.adapters.orm.sqlalchemy.adapters import AsyncSqlAlchemyAdapter, SqlAlchemyAdapter
from archipy.adapters.orm.sqlalchemy.session_manager_mocks import AsyncSessionManagerMock, SessionManagerMock
from archipy.configs.config_template import SqlAlchemyConfig


class SqlAlchemyMock(SqlAlchemyAdapter):
    """Mock implementation of the SQLAlchemy adapter for testing.

    This class provides an in-memory SQLite database for testing SQLAlchemy operations
    without requiring a real database connection. It uses the SessionManagerMock
    to manage the in-memory database sessions.

    Args:
        orm_config (SqlAlchemyConfig, optional): Custom SQLAlchemy configuration.
            If None, uses an in-memory SQLite database. Defaults to None.

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.mocks import SqlAlchemyMock
        >>> from archipy.models.entities import BaseEntity
        >>>
        >>> # Create a mock database for testing
        >>> db = SqlAlchemyMock()
        >>>
        >>> # Test entity creation
        >>> user = User(name="Test User", email="test@example.com")
        >>> db.create(user)
        >>>
        >>> # Test query operations
        >>> from sqlalchemy import select
        >>> query = select(User).where(User.name == "Test User")
        >>> results, count = db.execute_search_query(User, query)
        >>> assert count == 1
    """

    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        """Initializes the SQLAlchemy mock adapter.

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
        self.session_manager = SessionManagerMock(configs)


class AsyncSqlAlchemyMock(AsyncSqlAlchemyAdapter):
    """Asynchronous mock implementation of the SQLAlchemy adapter for testing.

    This class provides an in-memory SQLite database with async support for testing
    asynchronous SQLAlchemy operations without requiring a real database connection.
    It uses the AsyncSessionManagerMock to manage the in-memory database sessions.

    Args:
        orm_config (SqlAlchemyConfig, optional): Custom SQLAlchemy configuration.
            If None, uses an in-memory SQLite database with aiosqlite. Defaults to None.

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.mocks import AsyncSqlAlchemyMock
        >>> from archipy.models.entities import BaseEntity
        >>>
        >>> # Create a mock database for testing
        >>> db = AsyncSqlAlchemyMock()
        >>>
        >>> # Example async function using the mock adapter
        >>> async def test_user_creation():
        ...     user = User(name="Test User", email="test@example.com")
        ...     await db.create(user)
        ...     # Test query operations
        ...     from sqlalchemy import select
        ...     query = select(User).where(User.name == "Test User")
        ...     results, count = await db.execute_search_query(User, query)
        ...     assert count == 1
    """

    def __init__(self, orm_config: SqlAlchemyConfig | None = None) -> None:
        """Initializes the async SQLAlchemy mock adapter.

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
        self.session_manager = AsyncSessionManagerMock(configs)
