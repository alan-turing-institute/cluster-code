# Run tests on Urika

To run unit tests using `pytest`, run:

```bash
fab standalone.setup:query=queries/total_words.py,oids=$PWD/oids.txt
cd standalone
pytest
```

You should see:

```
============================= test session starts =============================
platform linux2 -- Python 2.7.13, pytest-3.7.1, py-1.5.4, pluggy-0.7.1
rootdir: /home/users/michaelj/cluster-code, inifile:
collected 11 items

bluclobber/test/test_archive.py ..                                      [ 18%]
bluclobber/test/test_book.py ........                                   [ 90%]
bluclobber/test/test_page.py .                                          [100%]

========================== 11 passed in 0.46 seconds ==========================
```
