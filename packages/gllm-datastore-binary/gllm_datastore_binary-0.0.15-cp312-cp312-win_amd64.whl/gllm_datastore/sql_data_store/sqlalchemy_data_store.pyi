from gllm_datastore.sql_data_store.sqlalchemy_sql_data_store import SQLAlchemySQLDataStore as SQLAlchemySQLDataStore

class SQLAlchemyDataStore(SQLAlchemySQLDataStore):
    """A data store for interacting with SQLAlchemy.

    This class is a subclass of SQLAlchemySQLDataStore.
    It is deprecated and will be removed in a future release.
    Use SQLAlchemySQLDataStore instead.
    """
