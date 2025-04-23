from bosa_core.authentication.database_migration.base_migration import DbMigration as DbMigration

def run_migrations(engine, current_version: int = 0):
    """Run database migrations to update the schema to the latest version.

    This function scans the migration_versions directory for migration files,
    sorts them by version number, and applies each migration in order if its
    version is greater than the current version.

    Args:
        engine: The database engine to use for running migrations.
        current_version (int): The current version of the database schema. Defaults to 0.
    """
