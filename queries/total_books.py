"""
Counts the total number of books.
"""


def do_query(archives, _, _log):
    """
    Counts the total number of books.
    """
    books = archives.flatMap(lambda archive: list(archive))
    result = books.count()
    return {"books": result}
