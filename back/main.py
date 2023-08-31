import functools

import fire

from ext import alembic_tools
from ports import rdbs, api
from config import DBConfig


def launch(db_config: DBConfig):
    import uvicorn
    app = api.v1.get_application(db_config)
    uvicorn.run(app, host="0.0.0.0", port=80)


if __name__ == "__main__":
    db_config = DBConfig()

    migrations_rdbs_args = dict(
        db_dsn=db_config.dsn,
        metadata=rdbs.generic.db_metadata,
        migrations_source=rdbs.migrations,
    )
    fire.Fire(
        {
            "api:run": lambda: launch(db_config),
            "rdbs:upgrade": functools.partial(
                alembic_tools.commands.upgrade, **migrations_rdbs_args
            ),
            "rdbs:downgrade": functools.partial(
                alembic_tools.commands.downgrade, **migrations_rdbs_args
            ),
            "rdbs:create_auto_migration": lambda message: functools.partial(
                alembic_tools.commands.create_auto_migration,
                message=message,
                offline=False,
                **migrations_rdbs_args,
            ),
            "rdbs:create_empty_migration": lambda message: functools.partial(
                alembic_tools.commands.create_empty_migration,
                message=message,
                **migrations_rdbs_args,
            ),
        }
    )
