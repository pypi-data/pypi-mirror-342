import pandas
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

from airflow.hooks.base_hook import BaseHook
# from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import reflection
from snowflake.sqlalchemy import VARIANT, URL

from datetime import date
from urllib.parse import quote_plus

def _retrieve_private_key(private_key_file, private_key_password):
    # Code copied from the Snowflake SQLAlchemy PyPi page
    # https://pypi.org/project/snowflake-sqlalchemy/
    with open(private_key_file, "rb") as key:
        p_key= serialization.load_pem_private_key(
            key.read(),
            password=private_key_password.encode(),
            backend=default_backend()
        )

    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())

    return pkb

def describe(table):
    for c in table.columns:
        tipe = c.type
        if isinstance(tipe, VARIANT):
             tipe = 'VARIANT'
        print('{}: {}'.format(c.name, tipe))

class Warehouse:
    """
    This class is an abstraction that allows you to connect to the Snowflake Warehouse.
    It has several methods that allow for easy access to the warehouse.
    -- execute: run some arbitrary SQL in the warehouse. totally safe!
    -- read_sql: execute a SELECT statement and return results as a pandas.DataFrame
    -- reflect: return a SQLAlchemy Table object containing metadata about the table

    This class also has a couple of SQLAlchemy-based instance variables
    - engine: contains information about how to connect to the warehouse
    - insp: a SQLAlchemy inspector object that lets query metadata about the warehouse
            e.g., Snowflake.insp.get_table_names('wild_west')
    """
    def __init__(self, engine):
        self.engine = engine
        self.meta = MetaData(bind=engine)
        self._insp = None
        self._conn = None
        self.loaded_tables = {}   # dictionary of Table objects keyed by "schema.table_name"

    @property
    def insp(self):
        if self._insp is None:
            self._insp = reflection.Inspector.from_engine(self.engine)
        return self._insp

    @property
    def conn(self):
        if self._conn is None:
            self._conn = self.engine.connect()
        return self._conn

    # caller is responsible for closing the connection when done
    def execute(self, sql):
        """
        execute: SQL statement -> (connection, proxy)

        Running the execute method sends the SQL string to the warehouse using
        this object's connection object. The return value is a tuple of the
        connection object and the SQLAlchemy proxy object returned from executing
        the SQL.
        """
        return self.conn, self.conn.execute(sql)

    def read_sql(self, sql):
        """
        read_sql: 'SELECT ...' -> pandas.DataFrame
        read_sql: SQLAlchemy select object -> pandas.DataFrame

        The warehouse read_sql method is a minimalist wrapper around the pandas.read_sql
        method. The sole argument to this method can either be a string (typically a SELECT statement)
        or an object constructed using SQLAlchemy's select method.
        """
        return pandas.read_sql(sql, self.engine)

    def reflect(self, table_or_view, schema):
        """
        reflect: table name, schema name (optional) -> SQLAlchemy Table object
        reflect: view name,  schema name (optional) -> SQLAlchemy Table object

        The reflect method is useful to grab the underlying metadata for a table in the warehouse.
        Using the returned value, you can print out the column names and types using the describe method.

        Note that if the table or view name has a '.' in it, then this method will try to infer the schema name
        and ignore the passed in argument

        t_table = Snowflake.reflect('users', schema='staging_scrapes')
        describe(t_table)
        """
        name_with_schema = '{schema}.{table_or_view}'.format(
            schema=schema,
            table_or_view=table_or_view
        )

        # if it's already been loaded, why bother loading it again? just return it
        table = self.loaded_tables.get(name_with_schema, None)
        if table is not None:
            return table

        table = Table(table_or_view, self.meta, autoload=True, schema=schema)

        # sets the column names explicitly on the instance so that tab-completion is easy
        for c in table.columns:
            setattr(table, 'c_{}'.format(c.name), c)

        # save so we don't have to load it again later
        self.loaded_tables[name_with_schema] = table

        return table
    
    def close(self):
        self.conn.close()




def create_warehouse(snowflake_conn_id="snowflake_default"):
    snowflake_conn = BaseHook.get_connection(snowflake_conn_id)
    extras_dict = snowflake_conn.extra_dejson

    account = extras_dict['account'].lower()
    database = extras_dict['database'].lower()
    password = snowflake_conn.password
    role = extras_dict.get('role', 'dataops').lower()
    schema = snowflake_conn.schema.lower() if isinstance(snowflake_conn.schema, str) else 'public'
    user = snowflake_conn.login
    warehouse = extras_dict['warehouse'].lower()
    
    if 'private_key_file' in extras_dict:
        pkb = _retrieve_private_key(extras_dict['private_key_file'], password)
        warehouse = Warehouse(
            create_engine(
                URL(
                    account=account,
                    warehouse=warehouse,
                    database=database,
                    schema=schema,
                    user=user,
                    role=role,
                ),
                connect_args={
                    'private_key': pkb,
                    },
                pool_size=1
            )
        )
                    
    else:
        warehouse = Warehouse(
            create_engine(
                URL(
                    account=account,
                    warehouse=warehouse,
                    database=database,
                    schema=schema,
                    user=user,
                    role=role,
                    password=password,
                ),
                pool_size=1
            )
        )
            
    return warehouse    