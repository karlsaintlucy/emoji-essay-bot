import os
import random
import sqlite3

from urllib.parse import urlparse

from db_connect import connect_to_db, disconnect_from_db

from count_emojis import count_emojis


def parse_message(text):
    words = text.split(' ')

    word_count = len(words)
    emoji_count = round(0.75 * word_count)
    new_word_count = word_count + emoji_count

    new_indices = random.sample(range(new_word_count), word_count)
    new_indices.sort()

    index_word_mapping = tuple(zip(new_indices, words))

    new_words = [None] * new_word_count

    for index, word in index_word_mapping:
        new_words[index] = word

    emojis_to_fetch = new_words.count(None)

    emojis = get_random_emojis(emojis_to_fetch)
    emoji = emoji_generator(emojis)

    for i in range(len(new_words)):
        if new_words[i] == None:
            new_words[i] = next(emoji)

    new_text = ' '.join(new_words)

    return new_text


def get_random_emojis(emojis_to_fetch):
    total_emoji_count = count_emojis()

    random_ids = []
    for i in range(emojis_to_fetch):
        random_id = random.randint(1, total_emoji_count)
        random_ids.append(random_id)

    emojis = []
    conn, c = connect_to_db()

    for random_id in random_ids:
        c.execute("""
            SELECT emoji FROM emojis WHERE id = %s;
        """, (random_id,))
        emoji = c.fetchone()[0]
        emojis.append(emoji)

    disconnect_from_db(conn, c)

    return emojis


def text_generator(words):
    for word in words:
        yield word


def emoji_generator(emojis):
    for emoji in emojis:
        yield emoji
