"""Scrape WebFX's Emoji Cheat Sheet and build db."""

import requests

from bs4 import BeautifulSoup

from db_connect import connect_to_db, disconnect_from_db

EMOJI_LIST_URL = 'http://fbemojis.com/'


def main():
    """Control the scraping process."""

    emojis = scrape_emojis(EMOJI_LIST_URL)

    if build_db(emojis):
        return True

    return False


def scrape_emojis(url):
    """Scrape the WebFX page for name strings."""

    response = requests.get(url)
    response_content = response.content
    soup = BeautifulSoup(response_content, 'html.parser')

    span_list = soup.find_all('span', 'part text')

    emojis = []
    for span in span_list:
        emoji = span(string=True)
        if emoji != []:
            emojis.append((emoji[0],))

    return emojis


def build_db(emojis):
    """Build the SQLite3 database."""

    conn, c = connect_to_db()

    c.execute("""
        CREATE TABLE IF NOT EXISTS emojis (
            id SERIAL PRIMARY KEY,
            emoji TEXT NOT NULL
        );
    """)

    c.executemany("""
        INSERT INTO emojis (emoji) VALUES (%s);
    """, emojis)

    conn.commit()

    disconnect_from_db(conn, c)

    return True


if __name__ == '__main__':
    main()
