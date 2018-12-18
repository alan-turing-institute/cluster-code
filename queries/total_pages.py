'''
This module counts the total number of pages across all books.
'''

from operator import add
import re

from bluclobber.archive import Archive
from bluclobber.sparkrods import get_streams

import yaml
import sys


def do_query(archives, _, _log):
    '''
    Get total number of pages across all books.
    '''
    books = archives.flatMap(lambda archive: list(archive))
    page_counts = books.map(lambda book: book.pages)
    result = [books.count(), page_counts.reduce(lambda x,y: x+y)]
    return {"books": result[0], "pages": result[1]}
