def format_sql_query(query: str) -> str:
    """Format the SQL query to ensure it is correctly structured.

    Removes the code block markdown from the SQL query and trims any leading or trailing whitespace.

    Args:
        query (str): The SQL query output from the language model.

    Returns:
        str: The formatted SQL query.
    """
def validate_query(query: str, dialect: str = 'postgres') -> None:
    '''Validates if the given string is an SQL statement using sqlglot.

    Args:
        query (str): The SQL query to be validated.
        dialect (str, optional): The SQL dialect to be used for validation. Defaults to "postgres".

    Raises:
        ValueError: If the query is not a valid SQL statement.
    '''
