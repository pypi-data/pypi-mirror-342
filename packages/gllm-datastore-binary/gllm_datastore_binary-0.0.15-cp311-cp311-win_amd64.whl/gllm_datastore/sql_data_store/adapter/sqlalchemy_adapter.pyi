from _typeshed import Incomplete
from sqlalchemy.engine import Engine as Engine

class SQLAlchemyAdapter:
    """Initializes a database engine and session using SQLAlchemy.

    Provides a scoped session and a base query property for interacting with the database.

    Attributes:
        engine (Engine): The SQLAlchemy engine object.
        db (Session): The SQLAlchemy session object.
        base (DeclarativeMeta): The SQLAlchemy declarative base object.
    """
    engine: Incomplete
    db: Incomplete
    base: Incomplete
    @classmethod
    def initialize(cls, engine_or_url: Engine | str, pool_size: int = 50, max_overflow: int = 0, autocommit: bool = False, autoflush: bool = True):
        """Creates a new database engine and session.

        Must provide either an engine or a database URL.

        Args:
            engine_or_url (Engine | str): Sqlalchemy engine object or database URL.
            pool_size (int, optional): The size of the database connections to be maintained. Defaults to 50.
            max_overflow (int, optional): The maximum overflow size of the pool. Defaults to 0.
            autocommit (bool, optional): If True, all changes to the database are committed immediately.
                Defaults to False.
            autoflush (bool, optional): If True, all changes to the database are flushed immediately. Defaults to True.
        """
