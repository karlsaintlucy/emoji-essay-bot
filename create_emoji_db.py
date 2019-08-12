"""Scrape Facebook Emojis page and build db."""

import requests

from bs4 import BeautifulSoup

from app import Emoji, db

EMOJI_LIST_URL = 'http://fbemojis.com/'


def main():
    """Control the scraping process."""

    emojis = scrape_emojis(EMOJI_LIST_URL)

    if build_db(emojis):
        print('Database built.')
        return True

    print('There was a problem building the database.')
    return False


def scrape_emojis(url):
    """Scrape the Facebook Emojis page for name strings."""

    response = requests.get(url)
    response_content = response.content
    soup = BeautifulSoup(response_content, 'html.parser')

    # All emoji characters are enclosed in <span class="part text"></span> tags.
    span_list = soup.find_all('span', 'part text')

    emojis = []
    for span in span_list:
        emoji = span(string=True)
        if emoji != []:
            emojis.append(emoji[0])

    return emojis


def build_db(emojis):
    """Add the emojis to the database."""

    for emoji in emojis:
        new_emoji = Emoji(emoji=emoji)
        db.session.add(new_emoji)  # pylint:disable=no-member

    db.session.commit()  # pylint:disable=no-member

    return True


if __name__ == '__main__':
    main()
