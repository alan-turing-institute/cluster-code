# Run tests locally

To run unit tests using `fab`, run:

```bash
fab standalone.setup:query=queries/total_words.py,oids=$PWD/oids.txt standalone.pytest
```

You should see:

```bash
============================= test session starts ==============================
platform linux2 -- Python 2.7.14, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
rootdir: /home/centos/cluster-code, inifile:
collected 11 items                                                             

bluclobber/test/test_archive.py ..                                       [ 18%]
bluclobber/test/test_book.py ........                                    [ 90%]
bluclobber/test/test_page.py .                                           [100%]

========================== 11 passed in 0.20 seconds ===========================
```

To run unit tests using `pytest`, run:

```bash
cd standalone
pytest
```
