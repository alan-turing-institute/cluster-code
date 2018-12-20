"""
Counts the number of occurrences of words per-year and groups by
year.

The query expects a file with a list of the words to search for, one
per line.

Words are normalized, by removing all 'a-z|A-Z' characters before
comparing with the list of words to search for.

The result is of form, for example:

    YEAR:
    - [WORD, N]
    - [WORD, N]
    - ...
    YEAR:
    ...

Only words that occur one or more times are returned.
"""

from operator import add

import utils


def do_query(archives, words_file, logger=None):
    """
    Counts the number of occurrences of words per-year and groups by
    year.

    @param archives: Archives holding Books
    @type archives: pyspark.rdd.PipelinedRDD with Archives.
    @param words_file: File with list of words to search for,
    one per line
    @type words_file: str or unicode
    @param logger: Logger
    """
    search_words = []
    with open(words_file, "r") as f:
        search_words = [word.strip() for word in list(f)]

    books = archives.flatMap(
        lambda archive: [(book.year, book) for book in list(archive)])
    # [(YEAR, BOOK), ...]

    words = books.flatMap(
        lambda (year, book): [
            ((year, utils.normalize(word)), 1)
            for (_, word) in book.scan_words()
        ])
    # [((YEAR, WORD), 1), ...]

    num_matches = words.filter(
        lambda ((year, word), _): word in search_words)
    # [((YEAR, WORD), 1), ...]

    result = num_matches \
        .reduceByKey(add) \
        .map(lambda ((year, word), count): (year, (word, count))) \
        .groupByKey() \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
    # reduceByKey
    # [((YEAR, WORD), TOTAL), ...]
    # map
    # [((YEAR, (WORD, TOTAL)), ...]
    # groupByKey
    # [(YEAR, [(WORD, TOTAL), (WORD, TOTAL), ...], ...]
    # map
    # [(YEAR, [[WORD, TOTAL], [WORD, TOTAL], ...], ...]
    return result
