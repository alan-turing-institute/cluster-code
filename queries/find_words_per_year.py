"""
Counts the number of occurrences of words per-year. The query expects
a file with a list of the words to search for, one per line.
"""

from operator import add
import re


def do_query(archives, words_file, logger=None):
    """
    Counts the number of occurrences of words per-year. The query
    expects a file with a list of the words to search for, one per
    line.
    """
    with open(words_file, "r") as f:
        words = [re.compile(r'\b' + word.strip() + r'\b', re.I | re.U)
                 for word in list(f)]

    books = archives.flatMap(
        lambda archive: [(book.year, book) for book in list(archive)])
    # [(YEAR, BOOK), ...]

    pages = books.flatMap(
        lambda (year, book): [(year, page) for page in list(book)])
    # [(YEAR, PAGE), ...]

    matches = pages.flatMap(
        lambda (year, page):
        [((year, regex.pattern), regex.findall(page.content))
         for regex in words])
    # [((YEAR, WORD), MATCHES), ...]

    num_matches = matches.map(
        lambda (year_word, matches): (year_word, len(matches)))
    # [((YEAR, WORD), NNNN), ...]

    # TODO Add a filter to strip 0 matches.

    result = num_matches \
        .reduceByKey(add) \
        .map(lambda (year_word, count): (year_word[0],
                                         (year_word[1].replace(r'\b', ''),
                                          count))) \
        .groupByKey() \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
        # reduceByKey
        # [((YEAR, WORD), TOTAL), ...]
        # map
        # [((YEAR, (WORD, TOTAL)), ...]
        # grou[ByKey
        # [(YEAR, [(WORD, TOTAL), (WORD, TOTAL), ...], ...]
        # map
        # [(YEAR, [[WORD, TOTAL], [WORD, TOTAL], ...], ...]
    return result
