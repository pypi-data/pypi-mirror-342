from collections.abc import Iterable


def return_single_query_results(
    sql: str | Iterable[str],
    return_last: bool,
    split_statements: bool | None
) -> bool:
    """
    Determine when results of single query only should be returned.

    For compatibility reasons, the behaviour of the DBAPIHook is somewhat confusing.
    In some cases, when multiple queries are run, the return value will be an iterable (list) of results
    -- one for each query. However, in other cases, when single query is run, the return value will be just
    the result of that single query without wrapping the results in a list.

    The cases when single query results are returned without wrapping them in a list are as follows:

    a) sql is string and ``return_last`` is True (regardless what ``split_statements`` value is)
    b) sql is string and ``split_statements`` is False

    In all other cases, the results are wrapped in a list, even if there is only one statement to process.
    In particular, the return value will be a list of query results in the following circumstances:

    a) when ``sql`` is an iterable of string statements (regardless what ``return_last`` value is)
    b) when ``sql`` is string, ``split_statements`` is True and ``return_last`` is False

    :param sql: sql to run (either string or list of strings)
    :param return_last: whether last statement output should only be returned
    :param split_statements: whether to split string statements.
    :return: True if the hook should return single query results
    """
    if split_statements is not None:
        return isinstance(sql, str) and (return_last or not split_statements)

    return isinstance(sql, str) and return_last


def fetch_all_handler(cursor) -> list[tuple] | None:
    """Return results for DbApiHook.run()."""
    if not hasattr(cursor, "description"):
        raise RuntimeError(
            "The database we interact with does not support DBAPI 2.0. Use operator and "
            "handlers that are specifically designed for your database."
        )

    if cursor.description is not None:
        return cursor.fetchall()

    return None


def fetch_one_handler(cursor) -> list[tuple] | None:
    """Return first result for DbApiHook.run()."""
    if not hasattr(cursor, "description"):
        raise RuntimeError(
            "The database we interact with does not support DBAPI 2.0. Use operator and "
            "handlers that are specifically designed for your database."
        )
    if cursor.description is not None:
        return cursor.fetchone()

    return None