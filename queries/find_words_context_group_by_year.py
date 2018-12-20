"""
Gets contextual information about the occurences of words and
group by year.

The query expects a file with a list of the words to search for, one
per line.

Words are normalized, by removing all 'a-z|A-Z' characters before
comparing with the list of words to search for.

The result is of form, for example:

    YEAR:
    - { "title": TITLE,
        "place": PLACE,
        "publisher": PUBLISHER,
        "page": PAGE,
        "text": TEXT,
        "word": WORD }
    - { ... }
    ...
    YEAR:
    ...
"""

import utils


def do_query(archives, words_file, logger=None):
    """
    Gets contextual information about the occurences of words
    and group by year.

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
            (year, book, page, utils.normalize(word))
            for (page, word) in book.scan_words()
        ])
    # [(YEAR, BOOK, PAGE, WORD), ...]

    filtered_words = words.filter(
        lambda (year, book, page, word): word in search_words)
    # [(YEAR, BOOK, PAGE, WORD), ...]

    words_and_context = filtered_words.map(
        lambda (year, book, page, word):
        (year, {"title": book.title,
                "place": book.place,
                "publisher": book.publisher,
                "page": page.code,
                "text": page.content,
                "word": word}))
    # [(YEAR, { "title": TITLE,
    #           "place": PLACE,
    #           "publisher": PUBLISHER,
    #           "page": PAGE,
    #           "text": TEXT,
    #           "word": WORD }), ...]
    result = words_and_context \
        .groupByKey() \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
    # groupByKey
    # [(YEAR, [ { "title": TITLE,
    #             "place": PLACE,
    #             "publisher": PUBLISHER,,
    #             "page": PAGE,
    #             "text": TEXT,
    #             "word": WORD }, ...], ...]
    # map
    # [(YEAR, [ { "title": TITLE,
    #             "place": PLACE,
    #             "publisher": PUBLISHER,,
    #             "page": PAGE,
    #             "text": TEXT,
    #             "word": WORD }, ...], ...]
    return result
