# Run queries

## Specify data files to query

Populate `files.txt` with the paths to the data files e.g.:

* Local:

```bash
find $HOME/dch -name "*.zip" > files.txt
```

* Urika:

```bash
find /mnt/lustre/<user>/dch -name "*.zip" > files.txt
```

Check:

```bash
cat files.txt
```

You should see the following:

* Local, where `<HOME>` is the path to your home directory, where you mounted the data:

```
<HOME>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip
<HOME>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip
...
```

* Urika:

```
/mnt/lustre/<user>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip
/mnt/lustre/<user>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip
...
```

---

## Specify a subset of data files to query

For experimentation, you may find it useful to run queries across a subset of the data. For example, you can hard-code the paths.

Alternatively, you can run `find` over a subset of the paths:

* Local:

```bash
find $HOME/dch/BritishLibraryBooks/1510_1699/ -name "*.zip" > files.txt
```

* Urika:

```bash
find /mnt/lustre/<user>/dch/BritishLibraryBooks/1510_1699/ -name "*.zip" > files.txt
```

---

## Run queries (general form)

Queries are run as follows, where `<QUERY>` is the name of a query and `<DATA>` the name of a complementary query-specific data file.

Create job for Spark:

```bash
fab standalone.prepare:query=queries/<QUERY>.py[,datafile=query_args/<DATA>.txt][,filenames=<PATH_TO_FILENAMES_FILE>]
```

`fab` sets up a `standalone` directory with the following format:

* `files.txt`: copy of <PATH_TO_FILENAMES_FILE>. Optional. Default: `files.txt`
* `bluclobber`: copy of `bluclobber`
* `bluclobber/query.py`: copy of `queries/<QUERY>.py`
* `input.data`: copy of `<DATA>.txt`. Whether this is needed depends on what <<QUERY>.py` is being used.

Run using `pyspark` (local only):

```bash
cd standalone
pyspark < newsrods/standalone_runner.py
```

Run using `spark-submit`:

```bash
fab standalone.submit:num_cores=144
```

Run using `spark-submit` (alternative):

```bash
cd standalone
zip -r newsrods.zip newsrods/
nohup spark-submit --py-files bluclobber.zip bluclobber/standalone_runner.py 144 > log.txt &
```

**Note:**

* `144` is the number of cores requested for the job. This, with the number of cores per node, determines the number of workers/executors and nodes. For Urika, which has 36 cores per node, this would request 144/36 = 4 workers/executors and nodes.
* If omitted, this defaults to `1`.

Check results:

```bash
cd standalone
cat result.yml 
```

---

## Available queries

The available queries, which can be substituted into `<QUERY>`, include the following.

### Total books

Run:

```bash
fab standalone.prepare:query=queries/total_books.py,filenames=$PWD/files.txt standalone.submit:num_cores=144
```

Expected results:

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` only: `{books: 2}`
* Query over `1510_1699/` only:  `{books: 693}`
* Query over all books: `{books: 63701}`

The number of books should be equal to the number of ZIP files over which the query was run.

### Total pages

Run:

```bash
fab standalone.prepare:query=queries/total_pages.py,filenames=$PWD/files.txt standalone.submit:num_cores=144
```

Expected results:

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` only: `{books: 2, pages: 42}`
* Query over `1510_1699/` only:  `{books: 693, pages: 62768}`
* Query over all books: `{books: 63701, pages: 22044324}`

The number of books should be equal to the number of ZIP files over which the query was run.

The number of pages should be equal to the number of `<Page>` elements in each XML file in the `ALTO` subdirectories within each zip file. This can be validated as follows (for example)

```bash
mkdir tmp
cp /mnt/lustre/<user>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip .
cp /mnt/lustre/<user>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip .
unzip 000000874_0_1-22pgs__570785_dat.zip
unzip 000001143_0_1-20pgs__560409_dat.zip
grep \<Page ALTO/*xml|wc -l
```
```
42
```

### Total words

Run:

```bash
fab standalone.prepare:query=queries/total_words.py,filenames=$PWD/files.txt standalone.submit:num_cores=144
```

Expected results:

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` only: `{books: 2, words: 4372}`
* Query over `1510_1699/` only: `{books: 693, words: 17479341}`
* Query over all books: `{books: 63701, words: 6866559285}`

The number of books should be equal to the number of ZIP files over which the query was run.

The number of words should be equal to the number of `<String>` elements in each XML file in the `ALTO` subdirectories within each zip file. This can be validated as follows (for example)

```bash
mkdir tmp
cp /mnt/lustre/<user>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip .
cp /mnt/lustre/<user>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip .
unzip 000000874_0_1-22pgs__570785_dat.zip
unzip 000001143_0_1-20pgs__560409_dat.zip
grep \<String ALTO/*xml|wc -l
```
```
4372
```

### Words grouped by year

Run:

```
fab standalone.prepare:query=queries/find_words_group_by_year.py,datafile=query_args/<WORDS>.txt,filenames=~/samples/oids.2books.txt standalone.submit:num_cores=144
```

where `<WORDS>.txt` is a file with a list of words to search for, one per line. Words in the books are converted to lower-case and non 'a-z' characters (e.g. commas, hyphens etc.) removed.

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `query_args/hearts.txt`:

```
1676:
- [hearts, 1]
- [heart, 4]
```

### Words grouped by word

Run:

```
fab standalone.prepare:query=queries/find_words_group_by_word.py,datafile=query_args/<WORDS>.txt,filenames=~/samples/oids.2books.txt standalone.submit:num_cores=144
```

where `<WORDS>.txt` is a file with a list of words to search for, one per line. Words in the books are converted to lower-case and non 'a-z' characters (e.g. commas, hyphens etc.) removed.

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `query_args/hearts.txt`:

```
heart:
- [1676, 4]
hearts:
- [1676, 1]
```

* Query over `1510_1699/` with `query_args/diseases.txt`:

```bash
wc results.yml
```
```
 67 189 791
```

* Query over all books with `query_args/diseases.txt`:

```bash
wc results.yml
```
```
 1226  3652 15784
```

### Normalize

Count total number of books, pages, words. This can be useful if wanting to see how the average number of books, pages and words change over time.

Run:

```
fab standalone.prepare:query=queries/normalize.py,filenames=$PWD/files.txt standalone.submit:num_cores=144
```

* Query over `1510_1699/`:

```bash
wc results.yml
```
```
 67 189 791
```
```bash
head results.yml
```
```
cancer:
- [1681, 1]
- [1667, 1]
- [1655, 1]
- [1644, 1]
- [1677, 1]
- [1658, 1]
- [1651, 2]
- [1684, 3]
- [1695, 5]
...
```

* Query over all books:

```bash
wc results.yml
```
```
 1226  3652 15784
```
```bash
head results.yml
```
```
cancer:
- [1681, 1]
- [1761, 2]
- [1849, 78]
- [1791, 8]
- [1744, 2]
- [1824, 39]
- [1834, 52]
- [1838, 50]
- [1749, 1]
...
```

---

## Check number of executors used

A quick-and-dirty way to get this number is to run:

```bash
grep Exec log.txt | wc -l
```

---

## Troubleshooting: `ImportError: No module named api`

If running `fab` you see:

```bash
ImportError: No module named api
```

Then check your version of `Fabric` e.g.

```bash
pip freeze | grep Fabric
```

It should be 1.x e.g. 1.14.0 and not 2.x. Fabric changed between version 1 and 2. See [fabric](https://github.com/fabric/fabric/issues/1743) issue [no module named fabric.api#1743](https://github.com/fabric/fabric/issues/1743).

---

## Troubleshooting: `pyspark: command not found`

If running `fab standalone` locally you get:

```bash
/bin/sh: pyspark: command not found
...
Aborting.
```

Then add Apache Spark to your `PATH`:

```bash
export PATH=~/spark-2.3.0-bin-hadoop2.7/bin:$PATH
```

---

## Troubleshooting: `No such file or directory: ''`

If you get:

```
File "/home/users/<user>/cluster-code/standalone/bluclobber/sparkrods.py", line 25, in <lambda>
  streams = down.map(lambda x: open(x))
IOError: [Errno 2] No such file or directory: ''
```

then check for blank lines in `files.txt` and, if there are any, then remove them.
