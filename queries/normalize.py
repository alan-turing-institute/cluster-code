"""
Counts total number of books, pages, words. This can be useful if
wanting to how how the average number of books, pages and words change
over time.

The result is of form, for example:

    YEAR: [BOOKS, PAGES, WORDS]
    YEAR: [BOOKS, PAGES, WORDS]
    ...
"""


def do_query(archives, _, _log):
    """
    Counts total number of books, pages, words.
    """
    books = archives.flatMap(lambda archive: list(archive))
    counts = books.map(lambda book: (book.year, (1, book.pages, len(list(book.words())))))
    # [(YEAR, (1, PAGES, WORDS)), ...]

    result = counts \
        .reduceByKey(lambda x, y: tuple(i + j for i, j in zip(x, y))) \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
        # reduceByKey
        # [(YEAR, (BOOKS, PAGES, WORDS)), ...]
        # map
        # [(YEAR, [BOOKS, PAGES, WORDS]), ...]
    return result
