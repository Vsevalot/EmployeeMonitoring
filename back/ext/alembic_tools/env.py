import alembic
import alembic.environment
import alembic.config
import sqlalchemy
import sqlalchemy.pool


def run_migrations_offline(
    context: alembic.environment.EnvironmentContext,
):
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    config: alembic.config.Config = context.config
    metadata: sqlalchemy.MetaData = config.attributes.get("metadata")

    url = config.get_main_option("sqlalchemy.url")
    version_table = config.attributes.get("version_table", "alembic_version")
    context.configure(
        url=url,
        target_metadata=metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table=version_table,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(
    context: alembic.environment.EnvironmentContext,
):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    config: alembic.config.Config = context.config
    metadata: sqlalchemy.MetaData = config.attributes.get("metadata")

    connectable = sqlalchemy.engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=sqlalchemy.pool.NullPool,
    )

    version_table = config.attributes.get("version_table", "alembic_version")
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=metadata,
            version_table=version_table,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations(
    context: alembic.environment.EnvironmentContext,
):
    if context.is_offline_mode():
        run_migrations_offline(
            context=context,
        )
    else:
        run_migrations_online(
            context=context,
        )


def main():
    context: alembic.environment.EnvironmentContext = alembic.context

    run_migrations(
        context=context,
    )


main()
