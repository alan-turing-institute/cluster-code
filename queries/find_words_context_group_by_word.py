"""
Gets contextual information about the occurences of words and
group by word.

The query expects a file with a list of the words to search for, one
per line.

Words are normalized, by removing all 'a-z|A-Z' characters before
comparing with the list of words to search for.

The result is of form, for example:

    WORD:
    - { "title": TITLE,
        "place": PLACE,
        "publisher": PUBLISHER,
        "page": PAGE,
        "text": TEXT,
        "year": YEAR }
    - { ... }
    ...
    WORD:
    ...
"""

import utils


def do_query(archives, words_file, logger=None):
    """
    Gets contextual information about the occurences of words
    and group by word.

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
        lambda archive: [book for book in list(archive)])
    # [BOOK, ...]

    words = books.flatMap(
        lambda book: [
            (book, page, utils.normalize(word))
            for (page, word) in book.scan_words()
        ])
    # [(BOOK, PAGE, WORD), ...]

    filtered_words = words.filter(
        lambda (book, page, word): word in search_words)
    # [(BOOK, PAGE, WORD), ...]

    words_and_context = filtered_words.map(
        lambda (book, page, word):
        (word, {"title": book.title,
                "place": book.place,
                "publisher": book.publisher,
                "page": page.code,
                "text": page.content,
                "year": book.year}))
    # [(WORD, { "title": TITLE,
    #           "place": PLACE,
    #           "publisher": PUBLISHER,
    #           "page": PAGE,
    #           "text": TEXT,
    #           "year": YEAR }), ...]
    result = words_and_context \
        .groupByKey() \
        .map(lambda (word, data): (word, list(data))) \
        .collect()
    # groupByKey
    # [(WORD, [ { "title": TITLE,
    #             "place": PLACE,
    #             "publisher": PUBLISHER,,
    #             "page": PAGE,
    #             "text": TEXT,
    #             "year": YEAR }, ...], ...]
    # map
    # [(WORD, [ { "title": TITLE,
    #             "place": PLACE,
    #             "publisher": PUBLISHER,,
    #             "page": PAGE,
    #             "text": TEXT,
    #             "year": YEAR }, ...], ...]
    return result
