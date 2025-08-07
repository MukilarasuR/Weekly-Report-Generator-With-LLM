from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Import your app's metadata and engine
from app.db.models import Base
from app.db.database import engine

# Alembic Config
config = context.config

# ✅ Set up Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Use Base.metadata from your models
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # ✅ Use the imported engine directly
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# ✅ Determine if offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
