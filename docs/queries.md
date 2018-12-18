# Run queries

## Specify data files to query

Populate `files.txt` with the paths to the data files e.g.:

* Local:

```bash
find $HOME/dch -name "*.zip" > files.txt
```

* Urika:

```bash
find /mnt/lustre/<your-urika-username>/dch -name "*.zip" > files.txt
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
/mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip
/mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip
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
find /mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/ -name "*.zip" > files.txt
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
* `query.py`: copy of `queries/<QUERY>.py`
* `input.data`: copy of `<DATA>.txt`. Whether this is needed depends on what <<QUERY>.py` is being used.

Run using `pyspark` (local only):

```bash
cd standalone
pyspark < query.py
```

Run using `spark-submit`:

```bash
fab standalone.submit:num_cores=144
```

Run using `spark-submit` (alternative):

```bash
cd standalone
zip -r newsrods.zip newsrods/
nohup spark-submit --py-files bluclobber.zip query.py 144 > log.txt &
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

Expected results, `number_of_books`:

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` only: 2
* Query over `1510_1699/` only: `693`
* Query over all books: `63701`

The number of books should be equal to the number of ZIP files over which the query was run.

### Total words

Run:

```bash
fab standalone.prepare:query=queries/total_words.py,filenames=$PWD/files.txt standalone.submit:num_cores=144
```

Expected results, `[number_of_books, number_of_words]`:

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` only: `[2, 4372]`
* Query over `1510_1699/` only: `[693, 17479341]`
* Query over all books: `[63701, 6866559285]`

The number of books should be equal to the number of ZIP files over which the query was run.

The number of words should be equal to the number of `<String>` elements in each XML file in the `ALTO` subdirectories within each zip file. This can be validated as follows (for example)

```bash
mkdir tmp
cp /mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip .
cp /mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip .
unzip 000000874_0_1-22pgs__570785_dat.zip
unzip 000001143_0_1-20pgs__560409_dat.zip
grep \<String ALTO/*xml|wc -l
```
```
4372
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
File "/home/users/michaelj/cluster-code/standalone/bluclobber/sparkrods.py", line 25, in <lambda>
  streams = down.map(lambda x: open(x))
IOError: [Errno 2] No such file or directory: ''
```

then check for blank lines in `files.txt` and, if there are any, then remove them.
