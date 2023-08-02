import os
import types
import typing

import alembic
import alembic.command
import alembic.config
import sqlalchemy

from . import (
    utils,
)

CONFIG_FAILED_MSG = (
    'Please provide one of "database_module" or ' '"metadata" and "migrations_source"'
)
VERSIONS_TABLE = "alembic_version"
SCRIPT_LOCATION = utils.abspath_for_script_directory()
DEFAULT_MIGRATIONS_FOLDER = "versions"
TRIGGER_MIGRATIONS_FOLDER = "triggers"
DATA_MIGRATIONS_FOLDER = "data_migrations"
FILE_TEMPLATE = "%%(year)d_%%(month).2d_%%(day).2d_%%(rev)s_%%(slug)s"


ModuleType = typing.Union[
    types.ModuleType,
    # FIXME: __init__.py не воспринимается как ModuleType
    typing.Any,
]
MigrationSourceType = typing.Union[
    str,
    ModuleType,
]


def _parse_config_parameters(
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
) -> typing.Tuple[sqlalchemy.MetaData, MigrationSourceType, str]:
    metadata = (
        getattr(database_module, "metadata", None)
        or getattr(database_module, "db_metadata", None)
        or metadata
    )
    migrations_source = (
        getattr(database_module, "migrations", None)
        or getattr(database_module, "db_migrations", None)
        or migrations_source
    )
    version_table = (
        getattr(database_module, "version_table", None)
        or getattr(database_module, "versions_table", None)
        or version_table
    )
    return metadata, migrations_source, version_table


def _get_migrations_dir(
    migrations_source: MigrationSourceType,
) -> str:
    if not isinstance(migrations_source, str):
        return utils.abspath_for_module(
            module=migrations_source,
        )
    return migrations_source


def _get_default_migrations_dir(
    migrations_dir: str,
) -> str:
    return os.path.join(migrations_dir, DEFAULT_MIGRATIONS_FOLDER)


def _get_trigger_migrations_dir(
    migrations_dir: str,
) -> str:
    return os.path.join(migrations_dir, TRIGGER_MIGRATIONS_FOLDER)


def _get_data_migrations_dir(
    migrations_dir: str,
) -> str:
    return os.path.join(migrations_dir, DATA_MIGRATIONS_FOLDER)


def _get_migrations_dirs(
    migrations_dir: str,
) -> str:
    default = _get_default_migrations_dir(
        migrations_dir=migrations_dir,
    )
    trigger = _get_trigger_migrations_dir(
        migrations_dir=migrations_dir,
    )
    data = _get_data_migrations_dir(
        migrations_dir=migrations_dir,
    )
    return f"{default} {trigger} {data}"


def get_config(
    db_dsn: str,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
) -> alembic.config.Config:
    metadata, migrations_source, version_table = _parse_config_parameters(
        database_module=database_module,
        metadata=metadata,
        migrations_source=migrations_source,
        version_table=version_table,
    )
    assert metadata and migrations_source, CONFIG_FAILED_MSG

    migrations_dir = _get_migrations_dir(
        migrations_source=migrations_source,
    )

    config = alembic.config.Config(
        attributes=dict(
            metadata=metadata,
            migrations_dir=migrations_dir,
            version_table=version_table,
        ),
    )

    config.set_main_option(
        name="script_location",
        value=SCRIPT_LOCATION,
    )
    config.set_main_option(
        name="file_template",
        value=FILE_TEMPLATE,
    )
    config.set_main_option(
        name="version_locations",
        value=_get_migrations_dirs(
            migrations_dir=migrations_dir,
        ),
    )
    config.set_main_option(
        name="sqlalchemy.url",
        value=db_dsn,
    )

    return config


def _do_create_revision(
    db_dsn: str,
    message: str,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
    migrations_folder: str = None,
    autogenerate: bool = False,
):
    config = get_config(
        db_dsn=db_dsn,
        database_module=database_module,
        version_table=version_table,
        migrations_source=migrations_source,
        metadata=metadata,
    )

    if migrations_folder is None:
        path = _get_default_migrations_dir(
            migrations_dir=config.attributes["migrations_dir"],
        )
    else:
        path = os.path.join(
            config.attributes["migrations_dir"],
            migrations_folder,
        )
    utils.mkdirs(path)

    alembic.command.revision(
        config,
        version_path=path,
        message=message,
        autogenerate=autogenerate,
    )


def create_revision(
    message: str,
    db_dsn: typing.Optional[str] = None,
    offline: bool = True,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
    migrations_folder: str = None,
    autogenerate: bool = False,
):
    """Создание миграции через низкоуровневый интерфейс"""
    if not offline and not db_dsn:
        raise EnvironmentError("Please provide DB DSN or use offline mode")

    try:
        if offline:
            upgrade(
                db_dsn=db_dsn,
                database_module=database_module,
                metadata=metadata,
                migrations_source=migrations_source,
                version_table=version_table,
            )

        _do_create_revision(
            db_dsn=db_dsn,
            message=message,
            database_module=database_module,
            metadata=metadata,
            migrations_source=migrations_source,
            version_table=version_table,
            migrations_folder=migrations_folder,
            autogenerate=autogenerate,
        )
    except Exception as e:
        print(e)


def create_auto_migration(
    message: str,
    db_dsn: typing.Optional[str] = None,
    offline: bool = True,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
):
    """Создание автоматической миграции на основе метаданных"""
    create_revision(
        db_dsn=db_dsn,
        version_table=version_table,
        message=message,
        autogenerate=True,
        database_module=database_module,
        metadata=metadata,
        migrations_source=migrations_source,
        offline=offline,
    )


def create_empty_migration(
    message: str,
    db_dsn: typing.Optional[str] = None,
    offline: bool = True,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
    migrations_folder: str = DEFAULT_MIGRATIONS_FOLDER,
):
    """Создание пустой миграции"""
    create_revision(
        db_dsn=db_dsn,
        version_table=version_table,
        message=message,
        migrations_folder=migrations_folder,
        autogenerate=False,
        database_module=database_module,
        metadata=metadata,
        migrations_source=migrations_source,
        offline=offline,
    )


def create_trigger_migration(
    message: str,
    db_dsn: typing.Optional[str] = None,
    offline: bool = True,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
):
    """Создание пустой миграции в каталоге миграций для триггеров"""
    create_revision(
        db_dsn=db_dsn,
        version_table=version_table,
        message=message,
        migrations_folder=TRIGGER_MIGRATIONS_FOLDER,
        autogenerate=False,
        database_module=database_module,
        metadata=metadata,
        migrations_source=migrations_source,
        offline=offline,
    )


def create_data_migration(
    message: str,
    db_dsn: typing.Optional[str] = None,
    offline: bool = True,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
):
    """Создание пустой миграции в каталоге для миграций данных"""
    create_revision(
        db_dsn=db_dsn,
        version_table=version_table,
        message=message,
        migrations_folder=DATA_MIGRATIONS_FOLDER,
        autogenerate=False,
        database_module=database_module,
        metadata=metadata,
        migrations_source=migrations_source,
        offline=offline,
    )


def create_merge_migration(
    db_dsn: str,
    message: str,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
    revisions: str = None,
):
    """Создание merge-миграции"""
    config = get_config(
        db_dsn=db_dsn,
        version_table=version_table,
        database_module=database_module,
        metadata=metadata,
        migrations_source=migrations_source,
    )

    alembic.command.merge(
        config,
        message=message,
        revisions=revisions or "heads",
    )


def upgrade(
    db_dsn: str,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
    version: str = "head",
):
    """Обновление базы данных до указанной версии"""
    config = get_config(
        db_dsn=db_dsn,
        version_table=version_table,
        database_module=database_module,
        metadata=metadata,
        migrations_source=migrations_source,
    )

    alembic.command.upgrade(
        config,
        revision=version,
    )


def downgrade(
    db_dsn: str,
    database_module: typing.Optional[ModuleType] = None,
    metadata: typing.Optional[sqlalchemy.MetaData] = None,
    migrations_source: typing.Optional[MigrationSourceType] = None,
    version_table: str = VERSIONS_TABLE,
    version: str = "-1",
):
    """Откат базы данных к казанной версии"""
    config = get_config(
        db_dsn=db_dsn,
        version_table=version_table,
        database_module=database_module,
        metadata=metadata,
        migrations_source=migrations_source,
    )

    alembic.command.downgrade(
        config,
        revision=version,
    )
