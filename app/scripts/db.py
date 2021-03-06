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


def main():
    """Create sqlite Discover Enhanced database."""
    database = r".\database\discover-enhanced.db"

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id integer PRIMARY KEY,
                                uid text NOT NULL,
                                name text NOT NULL,
                                join_date text
                            );"""

    sql_create_playlists_table = """CREATE TABLE IF NOT EXISTS playlists (
                                    id integer PRIMARY KEY,
                                    uid text NOT NULL,
                                    name text NOT NULL,
                                    user integer NOT NULL,
                                    scrape_date text NOT NULL,
                                    blob blob NOT NULL,
                                    FOREIGN KEY (user) REFERENCES users (id)
                                );"""

    sql_create_songs_table = """CREATE TABLE IF NOT EXISTS songs (
                                id integer PRIMARY KEY,
                                uid text NOT NULL,
                                name text NOT NULL,
                                album text NOT NULL,
                                blob blob NOT NULL
                            );"""

    sql_create_playlists_songs_table = """CREATE TABLE IF NOT EXISTS playlists_songs (
                                          id integer PRIMARY KEY,
                                          playlist_id integer NOT NULL,
                                          song_id integer NOT NULL,
                                          FOREIGN KEY (playlist_id) REFERENCES playlists (id),
                                          FOREIGN KEY (song_id) REFERENCES songs (id)
                                      );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_users_table)

        # create playlists table
        create_table(conn, sql_create_playlists_table)

        # create songs table
        create_table(conn, sql_create_songs_table)

        # create playlists_songs table
        create_table(conn, sql_create_playlists_songs_table)

        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
