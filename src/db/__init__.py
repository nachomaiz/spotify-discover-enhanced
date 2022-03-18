import sqlite3
from sqlite3 import Error

def create_connection(db_file: str):
    """Create database file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
            
    return conn
            

def create_table(conn: sqlite3.Connection, create_table_sql: str):
    """Create a table from the create_table_sql statement

    Parameters
    ----------
    conn : sqlite3.Connection
        Connection object
    create_table_sql : str
        a CREATE TABLE statement
    """
    if not create_table_sql.upper().startswith("CREATE TABLE"):
        raise Error("SQL does not start with `CREATE TABLE`.")
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
