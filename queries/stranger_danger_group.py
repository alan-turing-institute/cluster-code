from collections import defaultdict
from collections import deque
from itertools import islice
groups=[('stranger','danger')]
chunk_length=12

def mapper(book):
    finds=defaultdict(list)
    iterable=iter(book.scan_words())
    finding=deque(islice(iterable,0,chunk_length))
    for element in iterable:
        for group in groups:
            words=[normalize(word) for page, word in finding]
            contained=[target in words for target in group]
        if all(contained):
            finds[group].append([words, finding[0][0].code])
            for i in range(chunk_length):
                finding.popleft()
                element=iterable.next()
                finding.append(element)
        else:
            finding.popleft()
            finding.append(element)
    result = {group: [[book.title, book.publisher, book.year, book.code, content]]
            for group, content in finds.iteritems()}
    return result

reducer=merge_under(add)
