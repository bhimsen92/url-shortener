from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool


class DB:
    connection_pool = None

    @classmethod
    @contextmanager
    def get_db_session(cls):
        conn = cls.connection_pool.getconn()
        try:
            yield conn
        finally:
            cls.connection_pool.putconn(conn)


class DBMixin:
    @classmethod
    def execute(cls, query_type, query, *args):
        return_value = None
        with DB.get_db_session() as session:
            cursor = session.cursor()
            cursor.execute(query, args)
            if query_type == "get":
                return_value = cursor.fetchall()
            elif query_type == "post":
                session.commit()
            cursor.close()
        return return_value

    @classmethod
    def get(cls, query, *args):
        return cls.execute("get", query, *args)

    @classmethod
    def post(cls, query, *args):
        cls.execute("post", query, *args)


def setup_db(configuration):
    database_uri = "postgres://%s:%s@%s:%s/%s" % (
        configuration.db_user,
        configuration.db_password,
        configuration.db_host,
        configuration.db_port,
        configuration.db_name,
    )
    DB.connection_pool = ThreadedConnectionPool(1, 10, database_uri)
