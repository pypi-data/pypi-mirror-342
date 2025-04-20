from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class SessionManagerPort:
    """Interface for SQLAlchemy session management operations.

    This interface defines the contract for session management adapters,
    providing methods for retrieving and managing database sessions
    in a synchronous context.

    Implementing classes must provide mechanisms to:
    1. Retrieve a properly configured SQLAlchemy session
    2. Release/remove sessions when they're no longer needed

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.session_manager_ports import SessionManagerPort
        >>>
        >>> class CustomSessionManager(SessionManagerPort):
        ...     def __init__(self):
        ...         # Initialize session factory
        ...         self._session_factory = create_session_factory()
        ...
        ...     def get_session(self) -> Session:
        ...         return self._session_factory()
        ...
        ...     def remove_session(self) -> None:
        ...         # Cleanup logic
        ...         pass
    """

    @abstractmethod
    def get_session(self) -> Session:
        """Retrieve a SQLAlchemy session.

        This method provides a database session that can be used for
        querying, creating, updating, and deleting data.

        Returns:
            Session: A SQLAlchemy session object

        Examples:
            >>> session = session_manager.get_session()
            >>> results = session.query(User).all()
        """
        raise NotImplementedError

    @abstractmethod
    def remove_session(self) -> None:
        """Remove the current session from the registry.

        This method should be called to clean up the session when it's
        no longer needed, helping to prevent resource leaks and ensure
        proper session management.

        Examples:
            >>> try:
            ...     session = session_manager.get_session()
            ...     # Perform database operations
            ... finally:
            ...     session_manager.remove_session()
        """
        raise NotImplementedError


class AsyncSessionManagerPort:
    """Interface for asynchronous SQLAlchemy session management operations.

    This interface defines the contract for asynchronous session management adapters,
    providing methods for retrieving and managing database sessions in an
    asynchronous context using SQLAlchemy's async capabilities.

    Implementing classes must provide mechanisms to:
    1. Retrieve a properly configured asynchronous SQLAlchemy session
    2. Release/remove sessions asynchronously when they're no longer needed

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.session_manager_ports import AsyncSessionManagerPort
        >>>
        >>> class CustomAsyncSessionManager(AsyncSessionManagerPort):
        ...     def __init__(self):
        ...         # Initialize async session factory
        ...         self._session_factory = create_async_session_factory()
        ...
        ...     def get_session(self) -> AsyncSession:
        ...         return self._session_factory()
        ...
        ...     async def remove_session(self) -> None:
        ...         # Async cleanup logic
        ...         await self._session_factory.remove()
    """

    @abstractmethod
    def get_session(self) -> AsyncSession:
        """Retrieve an asynchronous SQLAlchemy session.

        This method provides an async database session that can be used for
        asynchronous querying, creating, updating, and deleting data.

        Returns:
            AsyncSession: An asynchronous SQLAlchemy session object

        Examples:
            >>> session = session_manager.get_session()
            >>> results = await session.execute(select(User))
            >>> users = results.scalars().all()
        """
        raise NotImplementedError

    @abstractmethod
    async def remove_session(self) -> None:
        """Asynchronously remove the current session from the registry.

        This method should be called to clean up the session when it's
        no longer needed, helping to prevent resource leaks and ensure
        proper session management in async contexts.

        Examples:
            >>> try:
            ...     session = session_manager.get_session()
            ...     # Perform async database operations
            ... finally:
            ...     await session_manager.remove_session()
        """
        raise NotImplementedError
