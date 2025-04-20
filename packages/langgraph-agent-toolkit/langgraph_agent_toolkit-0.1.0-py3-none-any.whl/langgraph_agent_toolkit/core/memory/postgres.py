from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from langgraph_agent_toolkit.core.memory.base import BaseMemoryBackend
from langgraph_agent_toolkit.core.settings import settings
from langgraph_agent_toolkit.helper.logging import logger


class PostgresMemoryBackend(BaseMemoryBackend):
    """PostgreSQL implementation of memory backend."""

    def validate_config(self) -> bool:
        """Validate that all required PostgreSQL configuration is present."""
        required_vars = [
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_HOST",
            "POSTGRES_PORT",
            "POSTGRES_DB",
        ]

        missing = [var for var in required_vars if not getattr(settings, var, None)]
        if missing:
            raise ValueError(
                f"Missing required PostgreSQL configuration: {', '.join(missing)}. "
                "These environment variables must be set to use PostgreSQL persistence."
            )
        return True

    def get_connection_string(self) -> str:
        """Build and return the PostgreSQL connection string from settings."""
        return (
            f"postgresql://{settings.POSTGRES_USER}:"
            f"{settings.POSTGRES_PASSWORD.get_secret_value()}@"
            f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
            f"{settings.POSTGRES_DB}"
        )

    @asynccontextmanager
    async def get_saver(self) -> AsyncGenerator[AsyncPostgresSaver, None]:
        """Asynchronous context manager for acquiring and releasing the PostgreSQL connection pool.

        Yields:
            AsyncPostgresSaver: The database saver instance

        """
        conn_string = self.get_connection_string()

        logger.info(
            f"Creating PostgreSQL connection pool: min_size={settings.POSTGRES_MIN_SIZE}, "
            f"max_size={settings.POSTGRES_POOL_SIZE}, max_idle={settings.POSTGRES_MAX_IDLE}"
        )

        # Use AsyncConnectionPool as an async context manager
        async with AsyncConnectionPool(
            conn_string,
            min_size=settings.POSTGRES_MIN_SIZE,
            max_size=settings.POSTGRES_POOL_SIZE,
            max_idle=settings.POSTGRES_MAX_IDLE,
            kwargs=dict(autocommit=True, prepare_threshold=0, row_factory=dict_row),
        ) as pool:
            logger.info("PostgreSQL connection pool opened successfully")

            try:
                yield AsyncPostgresSaver(conn=pool)
            finally:
                logger.info("PostgreSQL connection pool will be closed automatically")

    def get_checkpoint_saver(self) -> AbstractAsyncContextManager[AsyncPostgresSaver]:
        """Initialize and return a PostgreSQL saver instance."""
        self.validate_config()
        return self.get_saver()
