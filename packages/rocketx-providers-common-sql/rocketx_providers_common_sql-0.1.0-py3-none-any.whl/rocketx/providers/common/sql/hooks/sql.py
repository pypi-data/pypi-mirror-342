# encoding: utf8
import handlers
import sqlparse
from more_itertools import chunked
from datetime import datetime
from contextlib import closing, contextmanager, suppress
from functools import cached_property
from typing import Any, Literal, Optional, overload, Callable, TypeVar, cast, Protocol
from collections.abc import Generator, Iterable, Mapping, MutableMapping, Sequence

from rocketx.utils.log.logging_mixin import LoggingMixin

try:
    import pandas as pd
except ImportError:
    raise ImportError(
        "pandas library not installed, run: pip install 'apache-airflow-providers-common-sql[pandas]'."
    )

try:
    import polars as pl
except ImportError:
    raise ImportError(
        "polars library not installed, run: pip install 'apache-airflow-providers-common-sql[polars]'."
    )

T = TypeVar("T")


class ConnectorProtocol(Protocol):
    """Database connection protocol."""

    def connect(self, host: str, port: int, username: str, schema: str) -> Any:
        """
        Connect to a database.

        :param host: The database host to connect to.
        :param port: The database port to connect to.
        :param username: The database username used for the authentication.
        :param schema: The database schema to connect to.
        :return: the authorized connection object.
        """



class DbApiHook(LoggingMixin):
    """
    Abstract base class for sql hooks.

    When subclassing, maintainers can override the `_make_common_data_structure` method:
    This method transforms the result of the handler method (typically `cursor.fetchall()`) into
    objects common across all Hooks derived from this class (tuples). Most of the time, the underlying SQL
    library already returns tuples from its cursor, and the `_make_common_data_structure` method can be ignored.
    """
    # Override to have a default connection id for a particular dbHook
    default_conn_name = "default_conn_id"
    # Override if this db doesn't support semicolons in SQL queries
    strip_semicolon = False
    # Override if this db supports autocommit.
    supports_autocommit = False
    # Override if this db supports executemany.
    supports_executemany = False
    # Override with the object that exposes the connect method
    connector: ConnectorProtocol | None = None
    # Override with db-specific query to check connection
    _test_connection_sql = "SELECT 1"
    # Default SQL placeholder
    _placeholder: str = "%s"
    # _dialects: MutableMapping[str, MutableMapping] = resolve_dialects()
    # _resolve_target_fields = conf.getboolean("core", "dbapihook_resolve_target_fields", fallback=False)

    def __init__(
        self,
        conn_type: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        schema: Optional[str] = None,
        extra: Optional[dict] = None,
    ):
        super().__init__()
        self.conn_type = conn_type
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.extra = extra
        self.schema = schema

    @cached_property
    def placeholder(self) -> str:
        """Return SQL placeholder."""

    @property
    def insert_statement_format(self) -> str:
        """Return the insert statement format."""

    @property
    def replace_statement_format(self) -> str:
        """Return the replacement statement format."""

    @property
    def escape_word_format(self) -> str:
        """Return the escape word format."""

    @property
    def escape_column_names(self) -> bool:
        """Return the escape column names flag."""

    @property
    def connection(self):
        """Return the connection."""

    @connection.setter
    def connection(self, value: Any):
        """Set the connection."""

    
    def get_conn(self):
        raise NotImplementedError()


    def get_df(
        self, 
        sql: str,
        parameters: Optional[dict] = None,
        *,
        df_type: Literal["pandas", "polars"] = "pandas",
        **kwargs,
    ) -> pd.DataFrame | pl.DataFrame:
        """
        Execute the sql and returns a dataframe.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        :param df_type: Type of dataframe to return, either "pandas" or "polars"
        :param kwargs: (optional) passed into `pandas.io.sql.read_sql` or `polars.read_database` method
        """
        if df_type == "pandas":
            return self._get_pandas_df(sql, parameters, **kwargs)

        elif df_type == "polars":
            return self._get_polars_df(sql, parameters, **kwargs)

        else:
            raise ValueError(f"Invalid df_type: {df_type}, only 'pandas' or 'polars' are supported")


    def _get_pandas_df(
        self,
        sql: str,
        parameters: Optional[dict] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Execute the sql and returns a pandas dataframe.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        :param kwargs: (optional) passed into pandas.io.sql.read_sql method
        """
        with closing(self.get_conn()) as conn:
            return pd.read_sql(sql, conn, parameters=parameters, **kwargs)
        
    def _get_polars_df(
        self,
        sql,
        parameters: list | tuple | Mapping[str, Any] | None = None,
        **kwargs,
    ) -> pl.DataFrame:
        """
        Execute the sql and returns a polars dataframe.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        :param kwargs: (optional) passed into polars.read_database method
        """

        with closing(self.get_conn()) as conn:
            execute_options: dict[str, Any] | None = None
            if parameters is not None:
                if isinstance(parameters, Mapping):
                    execute_options = dict(parameters)
                else:
                    execute_options = {}

            return pl.read_database(sql, connection=conn, execute_options=execute_options, **kwargs)

    def get_df_by_chunks(
        self,
        sql,
        parameters: list | tuple | Mapping[str, Any] | None = None,
        *,
        chunksize: int,
        df_type: Literal["pandas", "polars"] = "pandas",
        **kwargs,
    ) -> Generator[pd.DataFrame | pl.DataFrame, None, None]:
        """
        Execute the sql and return a generator.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with
        :param chunksize: number of rows to include in each chunk
        :param df_type: Type of dataframe to return, either "pandas" or "polars"
        :param kwargs: (optional) passed into `pandas.io.sql.read_sql` or `polars.read_database` method
        """
        if df_type == "pandas":
            return self._get_pandas_df_by_chunks(sql, parameters, chunksize=chunksize, **kwargs)

        if df_type == "polars":
            return self._get_polars_df_by_chunks(sql, parameters, chunksize=chunksize, **kwargs)

        raise ValueError(f"Invalid df_type: {df_type}, only 'pandas' or 'polars' are supported")

    def _get_pandas_df_by_chunks(
        self,
        sql,
        parameters: list | tuple | Mapping[str, Any] | None = None,
        *,
        chunksize: int,
        **kwargs,
    ) -> Generator[pd.DataFrame, None, None]:
        """
        Execute the sql and return a generator.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with
        :param chunksize: number of rows to include in each chunk
        :param kwargs: (optional) passed into pandas.io.sql.read_sql method
        """
        with closing(self.get_conn()) as conn:
            yield from pd.read_sql(sql, con=conn, params=parameters, chunksize=chunksize, **kwargs)

    def _get_polars_df_by_chunks(
        self,
        sql,
        parameters: list | tuple | Mapping[str, Any] | None = None,
        *,
        chunksize: int,
        **kwargs,
    ) -> Generator[pl.DataFrame, None, None]:
        """
        Execute the sql and return a generator.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        :param chunksize: number of rows to include in each chunk
        :param kwargs: (optional) passed into pandas.io.sql.read_sql method
        """
        with closing(self.get_conn()) as conn:
            execute_options = None
            if parameters is not None:
                if isinstance(parameters, Mapping):
                    execute_options = dict(parameters)

            yield from pl.read_database(
                sql, connection=conn, execute_options=execute_options, batch_size=chunksize, **kwargs
            )

    def get_records(
        self,
        sql: str | list[str],
        parameters: Iterable | Mapping[str, Any] | None = None,
    ) -> Any:
        """
        Execute the sql and return a set of records.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        """
        return self.run(sql=sql, parameters=parameters, handler=handlers.fetch_all_handler)

    def get_first(self, sql: str | list[str], parameters: Iterable | Mapping[str, Any] | None = None) -> Any:
        """
        Execute the sql and return the first resulting row.

        :param sql: the sql statement to be executed (str) or a list of sql statements to execute
        :param parameters: The parameters to render the SQL query with.
        """
        return self.run(sql=sql, parameters=parameters, handler=handlers.fetch_one_handler)

    @staticmethod
    def strip_sql_string(sql: str) -> str:
        """Remove `;` of sql statement."""
        return sql.strip().rstrip(";")

    @staticmethod
    def split_sql_string(sql: str, strip_semicolon: bool = False) -> list[str]:
        """
        Split string into multiple SQL expressions.

        :param sql: SQL string potentially consisting of multiple expressions
        :param strip_semicolon: whether to strip semicolon from SQL string
        :return: list of individual expressions
        """
        splits = sqlparse.split(
            sql=sqlparse.format(sql, strip_comments=True),
            strip_semicolon=strip_semicolon,
        )
        return [s for s in splits if s]

    @property
    def last_description(self) -> Sequence[Sequence] | None:
        if not self.descriptions:
            return None
        return self.descriptions[-1]

    @overload
    def run(
        self,
        sql: str | Iterable[str],
        autocommit: bool = ...,
        parameters: Iterable | Mapping[str, Any] | None = ...,
        handler: None = ...,
        split_statements: bool = ...,
        return_last: bool = ...,
    ) -> None:
        ...

    @overload
    def run(
        self,
        sql: str | Iterable[str],
        autocommit: bool = ...,
        parameters: Iterable | Mapping[str, Any] | None = ...,
        handler: Callable[[Any], T] = ...,
        split_statements: bool = ...,
        return_last: bool = ...,
    ) -> tuple | list[tuple] | list[list[tuple] | tuple] | None:
        ...

    def run(
        self,
        sql: str | Iterable[str],
        autocommit: bool = False,
        parameters: Iterable | Mapping[str, Any] | None = None,
        handler: Callable[[Any], T] | None = None,
        split_statements: bool = False,
        return_last: bool = True,
    ) -> tuple | list[tuple] | list[list[tuple] | tuple] | None:
        """
        Run a command or a list of commands.

        Pass a list of SQL statements to the sql parameter to get them to
        execute sequentially.

        The method will return either single query results (typically list of rows) or list of those results
        where each element in the list are results of one of the queries (typically list of list of rows :D)

        For compatibility reasons, the behaviour of the DBAPIHook is somewhat confusing.
        In some cases, when multiple queries are run, the return value will be an iterable (list) of results
        -- one for each query. However, in other cases, when single query is run, the return value will
        be the result of that single query without wrapping the results in a list.

        The cases when single query results are returned without wrapping them in a list are as follows:

        a) sql is string and ``return_last`` is True (regardless what ``split_statements`` value is)
        b) sql is string and ``split_statements`` is False

        In all other cases, the results are wrapped in a list, even if there is only one statement to process.
        In particular, the return value will be a list of query results in the following circumstances:

        a) when ``sql`` is an iterable of string statements (regardless what ``return_last`` value is)
        b) when ``sql`` is string, ``split_statements`` is True and ``return_last`` is False

        After ``run`` is called, you may access the following properties on the hook object:

        * ``descriptions``: an array of cursor descriptions. If ``return_last`` is True, this will be
          a one-element array containing the cursor ``description`` for the last statement.
          Otherwise, it will contain the cursor description for each statement executed.
        * ``last_description``: the description for the last statement executed

        Note that query result will ONLY be actually returned when a handler is provided; if
        ``handler`` is None, this method will return None.

        Handler is a way to process the rows from cursor (Iterator) into a value that is suitable to be
        returned to XCom and generally fit in memory.

        You can use pre-defined handles (``fetch_all_handler``, ``fetch_one_handler``) or implement your
        own handler.

        :param sql: the sql statement to be executed (str) or a list of
            sql statements to execute
        :param autocommit: What to set the connection's autocommit setting to
            before executing the query.
        :param parameters: The parameters to render the SQL query with.
        :param handler: The result handler which is called with the result of each statement.
        :param split_statements: Whether to split a single SQL string into statements and run separately
        :param return_last: Whether to return result for only last statement or for all after split
        :return: if handler provided, returns query results (may be list of results depending on params)
        """
        self.descriptions = []

        if isinstance(sql, str):
            if split_statements:
                sql_list: Iterable[str] = self.split_sql_string(
                    sql=sql,
                    strip_semicolon=self.strip_semicolon,
                )
            else:
                sql_list = [sql] if sql.strip() else []
        else:
            sql_list = sql

        if sql_list:
            self.log.debug("Executing following statements against DB: %s", sql_list)
        else:
            raise ValueError("List of SQL statements is empty")
        _last_result = None
        with self._create_autocommit_connection(autocommit) as conn:
            with closing(conn.cursor()) as cur:
                results = []
                for sql_statement in sql_list:
                    self._run_command(cur, sql_statement, parameters)

                    if handler is not None:
                        result = self._make_common_data_structure(handler(cur))
                        if handlers.return_single_query_results(sql, return_last, split_statements):
                            _last_result = result
                            _last_description = cur.description
                        else:
                            results.append(result)
                            self.descriptions.append(cur.description)

            # If autocommit was set to False or db does not support autocommit, we do a manual commit.
            if not self.get_autocommit(conn):
                conn.commit()
            # Logs all database messages or errors sent to the client
            self.get_db_log_messages(conn)

        if handler is None:
            return None
        if handlers.return_single_query_results(sql, return_last, split_statements):
            self.descriptions = [_last_description]
            return _last_result
        return results

    def _make_common_data_structure(self, result: T | Sequence[T]) -> tuple | list[tuple]:
        """
        Ensure the data returned from an SQL command is a standard tuple or list[tuple].

        This method is intended to be overridden by subclasses of the `DbApiHook`. Its purpose is to
        transform the result of an SQL command (typically returned by cursor methods) into a common
        data structure (a tuple or list[tuple]) across all DBApiHook derived Hooks, as defined in the
        ADR-0002 of the sql provider.

        If this method is not overridden, the result data is returned as-is. If the output of the cursor
        is already a common data structure, this method should be ignored.
        """
        if isinstance(result, Sequence):
            return cast("list[tuple]", result)

        return cast("tuple", result)

    def _run_command(self, cur, sql_statement, parameters):
        """Run a statement using an already open cursor."""
        if self.log_sql:
            self.log.info("Running statement: %s, parameters: %s", sql_statement, parameters)

        if parameters:
            cur.execute(sql_statement, parameters)
        else:
            cur.execute(sql_statement)

        # According to PEP 249, this is -1 when query result is not applicable.
        if cur.rowcount >= 0:
            self.log.info("Rows affected: %s", cur.rowcount)

    def set_autocommit(self, conn, autocommit):
        """Set the autocommit flag on the connection."""
        if not self.supports_autocommit and autocommit:
            self.log.warning(
                "%s connection doesn't support autocommit but autocommit activated.",
                self.get_conn_id(),
            )
        conn.autocommit = autocommit

    def get_autocommit(self, conn) -> bool:
        """
        Get autocommit setting for the provided connection.

        :param conn: Connection to get autocommit setting from.
        :return: connection autocommit setting. True if ``autocommit`` is set
            to True on the connection. False if it is either not set, set to
            False, or the connection does not support auto-commit.
        """
        return getattr(conn, "autocommit", False) and self.supports_autocommit

    def get_cursor(self) -> Any:
        """Return a cursor."""
        return self.get_conn().cursor()

    def _generate_insert_sql(self, table, values, target_fields=None, replace: bool = False, **kwargs) -> str:
        """
        Generate the INSERT SQL statement.

        The REPLACE variant is specific to MySQL syntax, the UPSERT variant is specific to SAP Hana syntax

        :param table: Name of the target table
        :param values: The row to insert into the table
        :param target_fields: The names of the columns to fill in the table. If no target fields are
            specified, they will be determined dynamically from the table's metadata.
        :param replace: Whether to replace/upsert instead of insert
        :return: The generated INSERT or REPLACE/UPSERT SQL statement
        """
        if not target_fields and self._resolve_target_fields:
            with suppress(Exception):
                target_fields = self.dialect.get_target_fields(table)

        if replace:
            return self.dialect.generate_replace_sql(table, values, target_fields, **kwargs)

        return self.dialect.generate_insert_sql(table, values, target_fields, **kwargs)

    @contextmanager
    def _create_autocommit_connection(self, autocommit: bool = False):
        """Context manager that closes the connection after use and detects if autocommit is supported."""
        with closing(self.get_conn()) as conn:
            if self.supports_autocommit:
                self.set_autocommit(conn, autocommit)
            yield conn

    def insert_rows(
            self,
            table,
            rows,
            target_fields=None,
            commit_every=1000,
            replace=False,
            *,
            executemany=False,
            fast_executemany=False,
            autocommit=False,
            **kwargs,
    ):
        """
        Insert a collection of tuples into a table.

        Rows are inserted in chunks, each chunk (of size ``commit_every``) is
        done in a new transaction.

        :param table: Name of the target table
        :param rows: The rows to insert into the table
        :param target_fields: The names of the columns to fill in the table
        :param commit_every: The maximum number of rows to insert in one
            transaction. Set to 0 to insert all rows in one transaction.
        :param replace: Whether to replace instead of insert
        :param executemany: If True, all rows are inserted at once in
            chunks defined by the commit_every parameter. This only works if all rows
            have same number of column names, but leads to better performance.
        :param fast_executemany: If True, the `fast_executemany` parameter will be set on the
            cursor used by `executemany` which leads to better performance, if supported by driver.
        :param autocommit: What to set the connection's autocommit setting to
            before executing the query.
        """
        nb_rows = 0
        with self._create_autocommit_connection(autocommit) as conn:
            conn.commit()
            with closing(conn.cursor()) as cur:
                if self.supports_executemany or executemany:
                    if fast_executemany:
                        with suppress(AttributeError):
                            # Try to set the fast_executemany attribute
                            cur.fast_executemany = True
                            self.log.info(
                                "Fast_executemany is enabled for conn_id '%s'!",
                                self.get_conn_id(),
                            )

                    for chunked_rows in chunked(rows, commit_every):
                        values = list(
                            map(
                                lambda row_: self._serialize_cells(row_),
                                chunked_rows,
                            )
                        )
                        sql = self._generate_insert_sql(table, values[0], target_fields, replace, **kwargs)
                        self.log.debug("Generated sql: %s", sql)

                        try:
                            cur.executemany(sql, values)
                        except Exception as e:
                            self.log.error("Generated sql: %s", sql)
                            self.log.error("Parameters: %s", values)
                            raise e

                        conn.commit()
                        nb_rows += len(chunked_rows)
                        self.log.info("Loaded %s rows into %s so far", nb_rows, table)
                else:
                    for i, row in enumerate(rows, 1):
                        values = self._serialize_cells(row)
                        sql = self._generate_insert_sql(table, values, target_fields, replace, **kwargs)
                        self.log.debug("Generated sql: %s", sql)

                        try:
                            cur.execute(sql, values)
                        except Exception as e:
                            self.log.error("Generated sql: %s", sql)
                            self.log.error("Parameters: %s", values)
                            raise e

                        if commit_every and i % commit_every == 0:
                            conn.commit()
                            self.log.info("Loaded %s rows into %s so far", i, table)
                        nb_rows += 1
                    conn.commit()
        self.log.info("Done loading. Loaded a total of %s rows into %s", nb_rows, table)

    @classmethod
    def _serialize_cells(cls, row):
        return tuple(cls._serialize_cell(cell) for cell in row)

    @staticmethod
    def _serialize_cell(cell: str | datetime | None) -> str | None:
        """
        Return the SQL literal of the cell as a string.

        :param cell: The cell to insert into the table
        :return: The serialized cell
        """
        if cell is None:
            return None

        if isinstance(cell, datetime):
            return cell.isoformat()

        return str(cell)

    def bulk_dump(self, table, tmp_file):
        """
        Dump a database table into a tab-delimited file.

        :param table: The name of the source table
        :param tmp_file: The path of the target file
        """
        raise NotImplementedError()

    def bulk_load(self, table, tmp_file):
        """
        Load a tab-delimited file into a database table.

        :param table: The name of the target table
        :param tmp_file: The path of the file to load into the table
        """
        raise NotImplementedError()

    def test_connection(self):
        """Tests the connection using db-specific query."""
        status, message = False, ""
        try:
            if self.get_first(self._test_connection_sql):
                status = True
                message = "Connection successfully tested"
        except Exception as e:
            status = False
            message = str(e)

        return status, message

    def get_db_log_messages(self, conn) -> None:
        """
        Log all database messages sent to the client during the session.

        :param conn: Connection object
        """
