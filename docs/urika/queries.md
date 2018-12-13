# Run queries on Urika

## Update data directory (optional)

By default `deploy/urika.sh` looks for data in

```
/mnt/lustre/$USER/dch/BritishLibraryBooks
```

Edit this path if you want to use a different location.

---

## Update execution script to query a subset of books (optional)

For experimentation, you may find it useful to run queries across a subset of the data. This can be configured as follows. For example, to edit `deploy/urika.sh` to only query all books in `1510_1699/`:

Change:

```bash
for i in $remote_directory/*; do
```

to:

```bash
for i in $remote_directory/1510*; do
```

---

## Run queries (general form)

Queries are run as follows, where `<QUERY>` is the name of a query:

```bash
fab urika.setup:query=queries/<QUERY>.py urika.run:query_name=<QUERY>
```

When processing is complete, there will be one data file in `production/bluclobber/harness/output_<QUERY-NAME>/` per period (e.g. 1510-1699, etc.) For example:

```
production/bluclobber/harness/output_<QUERY>/out_1510_1699_0.yml
production/bluclobber/harness/output_<QUERY>/out_1700_1799_0.yml
...
```

**Note:** `production/` is deleted and recreated when running subsequent queries, so copy any query results you want to keep before running subsequent queries.

---

## Check query status

Data is processed as a background task using a combination of Mesos job submission to the compute nodes, and execution of MPI-enabled Python code on the compute nodes.

After you have set a query running, you can check if the processing has completed, by checking the running processes:

```bash
ps
```

If processing is still ongoing, this will show the following running processes:

```
   PID TTY          TIME CMD
...
105805 pts/2    00:00:00 urika.sh
105810 pts/2    00:00:00 mrun
105811 pts/2    00:00:00 mrun.py
...
```

You can also check the log file:

```bash
tail production/bluclobber/harness/output_submission
```

---

## Available queries

The available queries, which can be substituted into `<QUERY>`, include the following:

### Total books

Run query:

```bash
fab urika.setup:query=queries/total_books.py urika.run:query_name=total_books
```

**Note:** The log file will contain non-fatal errors as `urika.sh` tries to call non-existent `join_total_books.py` and `result_total_books.py` scripts.

Combine period-specific results into single results file:

```bash
python bluclobber/tools/join_values.py production/bluclobber/harness/output_total_books/ total_books.txt
```

Expected results, `number_of_books`:

* Query over `1510_1699/` only: `693`
* Query over all books: `163701`

### Total pages

Run query:

```bash
fab urika.setup:query=queries/total_pages.py urika.run:query_name=total_pages
```

**Note:** The log file will contain non-fatal errors as `urika.sh` tries to call non-existent `join_total_pages.py` and `result_total_pages.py` scripts.

Combine period-specific results into single results file:

```bash
python bluclobber/tools/join_lists.py production/bluclobber/harness/output_total_pages/ total_pages.txt
```

Expected results, `[number_of_books, number_of_pages]`:

* Query over `1510_1699/` only: `[693, 62768]`
* Query over all books: `[63701, 22044324]`

### Total words

Run query:

```bash
fab urika.setup:query=queries/total_words.py urika.run:query_name=total_words
```

**Note:** The log file will contain non-fatal errors as `urika.sh` tries to call non-existent `join_total_words.py` and `result_total_words.py` scripts.

Combine period-specific results into single results file:

```bash
python bluclobber/tools/join_lists.py production/bluclobber/harness/output_total_words/ total_words.txt
```

Expected results, `[number_of_books, number_of_words]`:

* Query over `1510_1699/` only: [693, 17479341]
* Query over all books: `[63701, 6866559285]`

### Normaliser

Create a derived dataset (counts of books, pages and words per year) to see how these change over time.

```bash
fab urika.setup:query=queries/normaliser.py urika.run:query_name=normaliser
```

On completion, `production/bluclobber/harness/data_normaliser/` contains a `normaliser.yml` file. This file is composed from period-specific results in `production/bluclobber/harness/output_normaliser/`.

Expected results, quick-and-dirty:

```bash
wc production/bluclobber/harness/data_normaliser/normaliser.yml
```
```
287 1148 7780 production/bluclobber/harness/data_normaliser/normaliser.yml
```

### Diseases

Search for references to the following diseases: cholera, tuberculosis, consumption, phthisis, typhoid, whooping, measles, typhus, smallpox, diarrhoea, dysentry, diphtheria, cancer.

```bash
fab urika.setup:query=queries/diseases.py urika.run:query_name=diseases
```

On completion, `production/bluclobber/harness/data_diseases/` contains a `.yml` file for each disease. These files are composed from period-specific results in `production/bluclobber/harness/output_diseases/`.

Expected results, quick-and-dirty:

```bash
wc production/bluclobber/harness/data_diseases/*.yml
```
```
   18   295  1497 production/bluclobber/harness/data_diseases/cancer.yml
   12   191  1036 production/bluclobber/harness/data_diseases/cholera.yml
   21   341  1804 production/bluclobber/harness/data_diseases/consumption.yml
    3    55   261 production/bluclobber/harness/data_diseases/diarrhoea.yml
    5    87   438 production/bluclobber/harness/data_diseases/diphtheria.yml
    6   103   480 production/bluclobber/harness/data_diseases/dysentry.yml
   13   211  1080 production/bluclobber/harness/data_diseases/measles.yml
  287  1148  7780 production/bluclobber/harness/data_diseases/normaliser.yml
   11   191   940 production/bluclobber/harness/data_diseases/phthisis.yml
   19   305  1582 production/bluclobber/harness/data_diseases/smallpox.yml
    5    79   381 production/bluclobber/harness/data_diseases/tuberculosis.yml
    9   151   767 production/bluclobber/harness/data_diseases/typhoid.yml
   13   207  1067 production/bluclobber/harness/data_diseases/typhus.yml
   13   223  1095 production/bluclobber/harness/data_diseases/whooping.yml
```

### Stranger and danger

Search for all occurrences of the string "stranger danger" or the words "stranger" and "danger" occurring within the same sentence.

```bash
fab urika.setup:query=queries/stranger_danger_group.py urika.run:query_name=stranger_danger_group
```

On completion, `production/bluclobber/harness/data/stranger_danger_group/` contains a `final.yml` file. This file is composed from period-specific results in `production/bluclobber/harness/output_stranger_danger_group/`. This file has the following structure:

```
(stranger, danger):
  - - <MODS:title> value
    - <MODS:publisher> value
    - <MODS:dateIssued> value
    - <MODS:recordIdentifier> value
    - - - <sentence>
        - <page>
      - - <sentence>
        - <page>
      ...
  - - <MODS:title> value
  ...
```

This can be processed in Python as follows:

```python
import yaml
with open("final.yml", "r") as f:
    data = yaml.load(f)
books = data['(stranger, danger)']

book = books[0]
title = book[0] # 'Poems ... viz. The Hermaphrodite. The Remedie of Love. Elegies. Sonnets, with other poems'
publisher = book[1] # 'Richard Hodgkinson, for W. W. and Laurence Blaikelocke'
dateIssued = book[2] # 1640
recordIdentifier = book[3] # '000241254'
matches = book[4]
match = matches[0]
sentence = match[0]
# ['stranger', '', 'loves', 'delight', 'and', 'sweetest', 'blisse', 'is', 'got', 'with', 'greatest', 'danger']
page = match[1] # '000070'
```

The source data for this result is in `1510_1699/000241254_0_1-90pgs__581128_dat.zip`, in the files:

* `000241254_metadata.xml`: title, publisher, dateIssued, recordIdentifier.
* `000241254_000070.xml`: page, sentence (composed from String elements).

---

## Sample query results

Data files with the expected query results can be found in the [epcc-master](https://github.com/alan-turing-institute/cluster-code-visualisations/tree/epcc-master) branch of [alan-turing-institute/cluster-code-visualisations](https://github.com/alan-turing-institute/cluster-code-visualisations) in the following directories:

### Diseases

[diseases/data](https://github.com/alan-turing-institute/cluster-code-visualisations/tree/epcc-master/diseases/data), data generated by EPCC running on Urika.

[diseases/data-ucl](https://github.com/alan-turing-institute/cluster-code-visualisations/tree/epcc-master/diseases/data-ucl), data originally generated by UCL.

You can compare your results to those in `visualisations` using the `bluclobber/tools/compare.py` script e.g.

```bash
python bluclobber/tools/compare.py production/bluclobber/harness/data_diseases/whooping.yml ~/visualisations/diseases/data-ucl/whooping.yml
```
```
/home/users/<your-urika-username>/visualisations/diseases/data-ucl/whooping.yml production/bluclobber/harness/data_diseases/whooping.yml
1920: 1 (/home/users/<your-urika-username>/visualisations/diseases/data-ucl/whooping.yml)
1899: 31 (/home/users/<your-urika-username>/visualisations/diseases/data-ucl/whooping.yml)
None: 47 (/home/users/<your-urika-username>/visualisations/diseases/data-ucl/whooping.yml)
1882: 69 =/= 72
```

This output shows that 3 key-values were found in one file but not the other, and one key had different values in each file.

### Stranger and danger

[stranger_danger](https://github.com/alan-turing-institute/cluster-code-visualisations/tree/epcc-master/stranger_danger), data generated by EPCC running on Urika.

---

## Visualise query results

To visualise the query results, see the [epcc-master](https://github.com/alan-turing-institute/cluster-code-visualisations/tree/epcc-master) branch of [alan-turing-institute/cluster-code-visualisations](https://github.com/alan-turing-institute/cluster-code-visualisations).

---
