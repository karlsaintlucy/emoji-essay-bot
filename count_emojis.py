import sqlite3

from db_connect import connect_to_db, disconnect_from_db


def count_emojis():
    """Run a query to get the total number of emojis."""

    conn, c = connect_to_db()

    c.execute("""
        SELECT COUNT(*) FROM emojis;
    """)
    count = c.fetchone()[0]

    disconnect_from_db(conn, c)

    return count


if __name__ == '__main__':
    count_emojis()
