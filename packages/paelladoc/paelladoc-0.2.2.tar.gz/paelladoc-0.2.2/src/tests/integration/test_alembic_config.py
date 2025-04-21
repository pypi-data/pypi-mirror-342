"""Integration tests for Alembic configuration."""

import os
import pytest
from pathlib import Path
import uuid
import asyncio
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from paelladoc.config.database import get_db_path

@pytest.fixture
def clean_env():
    """Remove relevant environment variables before each test."""
    original_db_path = os.environ.get("PAELLADOC_DB_PATH")
    original_env = os.environ.get("PAELLADOC_ENV")
    
    if "PAELLADOC_DB_PATH" in os.environ:
        del os.environ["PAELLADOC_DB_PATH"]
    if "PAELLADOC_ENV" in os.environ:
        del os.environ["PAELLADOC_ENV"]
    
    yield
    
    if original_db_path is not None:
        os.environ["PAELLADOC_DB_PATH"] = original_db_path
    if original_env is not None:
        os.environ["PAELLADOC_ENV"] = original_env

@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    test_db_name = f"test_alembic_{uuid.uuid4()}.db"
    test_dir = Path(__file__).parent / "temp_dbs"
    test_db_path = test_dir / test_db_name
    test_db_path.parent.mkdir(parents=True, exist_ok=True)
    
    yield test_db_path
    
    # Cleanup
    try:
        if test_db_path.exists():
            os.remove(test_db_path)
        test_db_path.parent.rmdir()
    except Exception as e:
        print(f"Error during cleanup: {e}")

@pytest.fixture
def alembic_config(temp_db_path):
    """Create Alembic config for testing."""
    config = Config()
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{temp_db_path}")
    return config

def test_alembic_config_uses_db_path(clean_env, temp_db_path):
    """Test that Alembic uses the configured database path."""
    os.environ["PAELLADOC_DB_PATH"] = str(temp_db_path)
    
    from alembic.config import Config
    from alembic import command
    
    # Create config and get URL
    config = Config("alembic.ini")
    url = config.get_main_option("sqlalchemy.url")
    
    assert url == f"sqlite+aiosqlite:///{temp_db_path}"

@pytest.mark.asyncio
async def test_alembic_migrations_work_with_config(clean_env, temp_db_path, alembic_config):
    """Test that migrations work with the configured database."""
    from alembic import command
    
    # Set environment variable to use our test database
    os.environ["PAELLADOC_DB_PATH"] = str(temp_db_path)
    
    # Create async engine
    engine = create_async_engine(f"sqlite+aiosqlite:///{temp_db_path}")
    
    # Run migrations
    command.upgrade(alembic_config, "head")
    
    # Verify migrations applied
    async with engine.connect() as conn:
        # Get current revision
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()
        
        # Get latest revision from scripts
        script = ScriptDirectory.from_config(alembic_config)
        head_rev = script.get_current_head()
        
        assert current_rev == head_rev
    
    await engine.dispose()

@pytest.mark.asyncio
async def test_alembic_downgrade_works_with_config(clean_env, temp_db_path, alembic_config):
    """Test that downgrades work with the configured database."""
    from alembic import command
    
    # Set environment variable to use our test database
    os.environ["PAELLADOC_DB_PATH"] = str(temp_db_path)
    
    # Create async engine
    engine = create_async_engine(f"sqlite+aiosqlite:///{temp_db_path}")
    
    # Run migrations up
    command.upgrade(alembic_config, "head")
    
    # Run migrations down
    command.downgrade(alembic_config, "base")
    
    # Verify database is empty
    async with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        current_rev = context.get_current_revision()
        assert current_rev is None
    
    await engine.dispose()

def test_alembic_respects_environment_precedence(clean_env, temp_db_path):
    """Test that Alembic respects the environment variable precedence."""
    # Set both environment variables
    os.environ["PAELLADOC_DB_PATH"] = str(temp_db_path)
    os.environ["PAELLADOC_ENV"] = "development"
    
    from alembic.config import Config
    
    # Create config and get URL
    config = Config("alembic.ini")
    url = config.get_main_option("sqlalchemy.url")
    
    # Should use PAELLADOC_DB_PATH over development path
    assert url == f"sqlite+aiosqlite:///{temp_db_path}" 