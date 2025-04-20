from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from archipy.adapters.orm.sqlalchemy.session_manager_ports import AsyncSessionManagerPort, SessionManagerPort


class SessionManagerRegistry:
    """Registry for SQLAlchemy session managers.

    This registry provides a centralized access point for both synchronous and
    asynchronous session managers, implementing the Service Locator pattern.
    It lazily initializes the appropriate session manager when first requested.

    The registry maintains singleton instances of:
    - A synchronous session manager (SessionManagerAdapter)
    - An asynchronous session manager (AsyncSessionManagerAdapter)

    This allows different parts of an application to easily access the
    appropriate session manager without directly depending on concrete implementations.

    Examples:
        >>> from archipy.adapters.orm.sqlalchemy.session_manager_registry import SessionManagerRegistry
        >>>
        >>> # Get the default synchronous session manager
        >>> sync_manager = SessionManagerRegistry.get_sync_manager()
        >>> session = sync_manager.get_session()
        >>>
        >>> # Get the default asynchronous session manager
        >>> async_manager = SessionManagerRegistry.get_async_manager()
        >>> async_session = async_manager.get_session()
        >>>
        >>> # Use a custom session manager for testing
        >>> from archipy.adapters.orm.sqlalchemy.session_manager_mocks import SessionManagerMock
        >>> test_manager = SessionManagerMock()
        >>> SessionManagerRegistry.set_sync_manager(test_manager)
    """

    _sync_instance = None
    _async_instance = None

    @classmethod
    def get_sync_manager(cls) -> "SessionManagerPort":
        """Get the synchronous session manager instance.

        Lazily initializes a default SessionManagerAdapter if none has been set.

        Returns:
            SessionManagerPort: The registered synchronous session manager

        Examples:
            >>> manager = SessionManagerRegistry.get_sync_manager()
            >>> session = manager.get_session()
        """
        if cls._sync_instance is None:
            from archipy.adapters.orm.sqlalchemy.session_manager_adapters import SessionManagerAdapter

            cls._sync_instance = SessionManagerAdapter()
        return cls._sync_instance

    @classmethod
    def set_sync_manager(cls, manager: "SessionManagerPort") -> None:
        """Set a custom synchronous session manager.

        Use this method to override the default manager, particularly useful
        for testing or custom configuration scenarios.

        Args:
            manager: An instance implementing SessionManagerPort

        Examples:
            >>> from archipy.adapters.orm.sqlalchemy.session_manager_mocks import SessionManagerMock
            >>> SessionManagerRegistry.set_sync_manager(SessionManagerMock())
        """
        cls._sync_instance = manager

    @classmethod
    def get_async_manager(cls) -> "AsyncSessionManagerPort":
        """Get the asynchronous session manager instance.

        Lazily initializes a default AsyncSessionManagerAdapter if none has been set.

        Returns:
            AsyncSessionManagerPort: The registered asynchronous session manager

        Examples:
            >>> manager = SessionManagerRegistry.get_async_manager()
            >>> session = manager.get_session()
        """
        if cls._async_instance is None:
            from archipy.adapters.orm.sqlalchemy.session_manager_adapters import AsyncSessionManagerAdapter

            cls._async_instance = AsyncSessionManagerAdapter()
        return cls._async_instance

    @classmethod
    def set_async_manager(cls, manager: "AsyncSessionManagerPort") -> None:
        """Set a custom asynchronous session manager.

        Use this method to override the default manager, particularly useful
        for testing or custom configuration scenarios.

        Args:
            manager: An instance implementing AsyncSessionManagerPort

        Examples:
            >>> from archipy.adapters.orm.sqlalchemy.session_manager_mocks import AsyncSessionManagerMock
            >>> SessionManagerRegistry.set_async_manager(AsyncSessionManagerMock())
        """
        cls._async_instance = manager

    @classmethod
    def reset(cls) -> None:
        """Reset the registry to its initial state.

        This method clears both registered managers, which is particularly
        useful when testing to ensure a clean state between test cases.

        Examples:
            >>> # In a test setup method
            >>> def setUp(self):
            ...     SessionManagerRegistry.reset()
            ...     # Configure test-specific managers
        """
        cls._sync_instance = None
        cls._async_instance = None
