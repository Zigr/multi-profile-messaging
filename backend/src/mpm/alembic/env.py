import os
import sys
from pathlib import Path
from logging.config import fileConfig
from dotenv import load_dotenv

from sqlalchemy import engine_from_config, pool
from alembic import context

from mpm.database import Base
import mpm.models as models  # noqa: E402

ENV_FILE=Path(__file__ + "../../../../../../.env").resolve()
load_dotenv(ENV_FILE)
# ensure our backend module is on PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name:
    fileConfig(config.config_file_name)

# **IMPORT YOUR MODELS SO THEY REGISTER ON Base.metadata**

# Import your Base
target_metadata = Base.metadata

def get_url():
    return os.getenv('DATABASE_URL', 'sqlite:///./app.db')

# override the URL from alembic.ini with our env var
config.set_main_option('sqlalchemy.url', get_url())

def run_migrations_offline():
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
