# An example analysis, for determining
# total number of books.
# Calculates #books.

from bluclobber.archive import Archive
from bluclobber.sparkrods import get_streams

import yaml

streams = get_streams(downsample = 4096)
issues = streams.map(Archive)
books = issues.flatMap(lambda x: list(x))

result = books.count()

with open('result.yml','w') as result_file:
    result_file.write(yaml.safe_dump(result))
