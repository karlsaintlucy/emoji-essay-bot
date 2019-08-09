import sqlite3

DB_NAME = 'emojis.db'


def count_emojis():
    """Run a query to get the total number of emojis."""

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT COUNT(*) FROM emojis
    """)
    count = c.fetchone()[0]

    conn.commit()
    conn.close()

    return count


if __name__ == '__main__':
    count_emojis()
