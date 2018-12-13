# Implementation notes

## Number of processes

By default, 16 processes are used by MPI, as specified in `urika.sh`.


```
NP='2'
```

The number of processes must be <= the number of ZIP files. If not then the following exception will appear in the `production/bluclobber/harness/output_submission` log file:

```
0/16 INFO: 2018-07-18 17:20:08,146 Mapped
Traceback (most recent call last):
  File "query.py", line 70, in <module>
8/16 INFO: 2018-07-18 17:20:08,146 Analysing by archive
  File "query.py", line 57, in query
    local_result=reduce(self.reducer, quantities)
TypeError:     result = corpus.analyse(mapper, reducer, downsample, byboo
k, shuffler=shuffler)
  File "../model/corpus.py", line 41, in analyse
  File "../model/corpus.py", line 41, in analyse
    main()
  File "query.py", line 30, in main
```

---

## normaliser, diseases and post-processing

`bluclubber/harness/join_normaliser.py` merges the results from each process (held in `production/bluclobber/harness/output_normaliser`) into a `joined_normaliser.yml` file in the same directory. However, this is a simple script that can result in duplicated keys in the joined files. For example:

```bash
grep 1735 production/bluclobber/harness/output_normaliser/joined_normaliser.yml
```
```
1735: [12, 1226, 347355]
1735: [1, 330, 87592]
```
```
grep 1735 production/bluclobber/harness/data_normaliser/normaliser.yml
```
```
1735:  [13, 1556, 434947]
```

`bluclobber/harness/result_normaliser.py` processes `joined_normaliser.yml` into a single file with one key per year. It handles any duplicated keys in `joined_normaliser.yml` by summing the values of the duplicates.

`bluclubber/harness/join_diseases.py` merges the results from each process (held in `production/bluclobber/harness/output_diseases`) into a collection of files `joined_YYYY_YYYY.yml (e.g. `joined_1510_1699.yml`) for each set of years, in the same directory. However, as for `join_normaliser` this is a simple script and can also result in duplicated keys in the joined files.

`bluclobber/harness/result_diseases.py` creates a single file for each type of disease, with one key per year. It handles duplicated keys by summing the values of the duplicates.
