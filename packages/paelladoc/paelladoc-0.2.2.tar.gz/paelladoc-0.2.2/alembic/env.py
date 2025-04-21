"""Alembic environment configuration."""

import asyncio
import nest_asyncio

from logging.config import fileConfig
import os
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from paelladoc.config.database import get_db_path

from sqlmodel import SQLModel

# this is the Alembic Config object
config = context.config

# Apply nest_asyncio patch to allow nested event loops
nest_asyncio.apply()

# Set the SQLAlchemy URL based on our configuration
db_path = get_db_path()
config.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{db_path}")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Clear metadata before importing models, especially for testing scenarios
SQLModel.metadata.clear()

# Import all models that need to be created
# This ensures SQLModel populates its metadata
from paelladoc.adapters.output.sqlite import db_models # Assuming models are in db_models.py
target_metadata = SQLModel.metadata # Use SQLModel's metadata

# Ensure tables are created with extend_existing=True
# We might not need this loop if SQLModel handles it or if clear() suffices
# for table in target_metadata.tables.values():
#     table.extend_existing = True 

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """In this scenario we need to create an AsyncEngine and run migrations."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Run the sync migration function in the async context
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection: Connection) -> None:
    # Perform migrations within a transaction
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
