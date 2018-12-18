'''
This module counts the total number of books.
'''

from operator import add
import re

from bluclobber.archive import Archive
from bluclobber.sparkrods import get_streams

import yaml
import sys


def do_query(archives, _, _log):
    '''
    Get total number of books.
    '''
    books = archives.flatMap(lambda archive: list(archive))
    result = books.count()
    return {"books": result}
