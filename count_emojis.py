from app import db, Emoji


def count_emojis():
    """Run a query to get the total number of emojis."""

    count = db.session.query(Emoji).count()  # pylint:disable=no-member

    return count


if __name__ == '__main__':
    count_emojis()
