# Run tests

## Using `fab` (local only)

To run unit tests using `fab`, run:

```bash
fab standalone.setup standalone.pytest
```

You should see:

```bash
============================= test session starts ==============================
platform linux2 -- Python 2.7.13, pytest-3.7.1, py-1.5.4, pluggy-0.7.1
rootdir: /home/users/<user>/cluster-code, inifile:
collected 11 items                                                             

bluclobber/test/test_archive.py ..                                       [ 18%]
bluclobber/test/test_book.py ........                                    [ 90%]
bluclobber/test/test_page.py .                                           [100%]

========================== 11 passed in 0.20 seconds ===========================
```

## Using `pytest`

To run unit tests using `pytest`, run:

```bash
cd standalone
pytest
```

You should see:

```
============================= test session starts =============================
platform linux2 -- Python 2.7.13, pytest-3.7.1, py-1.5.4, pluggy-0.7.1
rootdir: /home/users/<user>/cluster-code, inifile:
collected 11 items

bluclobber/test/test_archive.py ..                                      [ 18%]
bluclobber/test/test_book.py ........                                   [ 90%]
bluclobber/test/test_page.py .                                          [100%]

========================== 11 passed in 0.46 seconds ==========================
```
