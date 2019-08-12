import os
import random

from app import db, Emoji
from count_emojis import count_emojis


def parse_message(text):
    """Parse the message received from the Facebook user and generate response."""

    words = text.split(' ')
    word_count = len(words)

    # Determine the number of emojis as a ratio against word count.
    emoji_count = round(0.75 * word_count)
    new_word_count = word_count + emoji_count

    # Randomize a list of new indices for the existing words to go into.
    new_indices = random.sample(range(new_word_count), word_count)
    new_indices.sort()

    # Map the words to the new indices.
    index_word_mapping = tuple(zip(new_indices, words))

    # Create a new list of empty values the length of the new word list.
    new_words = [None] * new_word_count

    # Insert the words into their new indices.
    for index, word in index_word_mapping:
        new_words[index] = word

    # new_words at each index with None will be filled in with emojis.
    emojis_to_fetch = new_words.count(None)

    emojis = get_random_emojis(emojis_to_fetch)
    emoji = emoji_generator(emojis)

    for i in range(len(new_words)):
        if new_words[i] is None:
            new_words[i] = next(emoji)

    new_text = ' '.join(new_words)

    return new_text


def get_random_emojis(emojis_to_fetch):
    """Get random emojis from database by random id."""

    total_emoji_count = count_emojis()

    random_ids = []

    for i in range(emojis_to_fetch):  # pylint:disable=unused-variable
        random_id = random.randint(1, total_emoji_count)
        random_ids.append(random_id)

    emojis = []

    for random_id in random_ids:
        r = db.session.query(Emoji).get(random_id)   # pylint:disable=no-member
        emoji = r.emoji
        emojis.append(emoji)

    return emojis


def emoji_generator(emojis):
    """Yield the next emoji in the list of emojis."""

    for emoji in emojis:
        yield emoji
