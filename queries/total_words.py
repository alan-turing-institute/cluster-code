# An example analysis, for determining total number of words
# across all books.

from bluclobber.archive import Archive
from bluclobber.sparkrods import get_streams

import yaml
import sys

num_cores = 1
if len(sys.argv) > 1:
    num_cores = sys.argv[1]

streams = get_streams(downsample = 4096, num_cores = num_cores)
issues = streams.map(Archive)
books = issues.flatMap(lambda x: list(x))
word_counts = books.map(lambda x: len(list(x.words())))

result = [books.count(), word_counts.reduce(lambda x,y: x+y)]

with open('result.yml','w') as result_file:
    result_file.write(yaml.safe_dump(result))
