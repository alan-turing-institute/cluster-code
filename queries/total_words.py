'''
This module counts the total number of words across all books.
'''

from operator import add
import re

from bluclobber.archive import Archive
from bluclobber.sparkrods import get_streams

import yaml
import sys


def do_query(archives, _, _log):
    '''
    Get total number of words across all books.
    '''
    books = archives.flatMap(lambda archive: list(archive))
    word_counts = books.map(lambda book: len(list(book.words())))
    result = [books.count(), word_counts.reduce(lambda x,y: x+y)]
    return {"books": result[0], "words": result[1]}
