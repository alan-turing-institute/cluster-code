# Run queries

## Specify data files to query

Populate `oids.txt` with the paths to the data files e.g.:

* Local:

```bash
find $HOME/dch -name "*.zip" > oids.txt
```

* Urika:

```bash
find /mnt/lustre/<your-urika-username>/dch -name "*.zip" > oids.txt
```

Check:

```bash
cat oids.txt
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

For experimentation, you may find it useful to run queries across a subset of the data. For examplnm you can hard-code the paths.

Alternatively, you can run `find` over a subset of the paths:

* Local:

```bash
find $HOME/dch/BritishLibraryBooks/1510_1699/ -name "*.zip" > oids.txt
```

* Urika:

```bash
find /mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/ -name "*.zip" > oids.txt
```

---

## Run queries (general form)

Queries are run as follows, where `<QUERY>` is the name of a query.

Create job for Spark:

```bash
fab standalone.setup:query=queries/<QUERY>.py,oids=$PWD/oids.txt
```

`fab` sets up a `standalone` directory with the following format:

* `bluclobber`: a copy of `bluclobber`.
* `query.py`: a copy of the `query` i.e. `queries/<QUERY>.py`.
* `oids.txt`: a copy of `oids.txt`.

Run using `pyspark` (local only):

```bash
cd standalone
pyspark < query.py
```

Run using `spark-submit`:

```bash
cd standalone
zip -r bluclobber.zip bluclobber/
nohup spark-submit --py-files bluclobber.zip query.py 144 > output_submission &
```

**Note:**

* `144` is the number of cores requested for the job. This, with the number of cores per node, determines the number of workers/executors and nodes. For Urika, which has 36 cores per node, this would request 144/36 = 4 workers/executors and nodes.
* If omitted, this defaults to `1`.

Check results:

```bash
cat result.yml 
```

---

## Available queries

The available queries, which can be substituted into `<QUERY>`, include the fol
lowing.

### Total books

Run:

```bash
fab standalone.setup:query=queries/total_books.py,oids=$PWD/oids.txt
cd standalone
zip -r bluclobber.zip bluclobber/
nohup spark-submit --py-files bluclobber.zip query.py 144 > output_submission &
```

Expected results, `number_of_books`:

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` only: 2
* Query over `1510_1699/` only: `693`
* Query over all books: `63701`

The number of books should be equal to the number of ZIP files over which the query was run.

### Total words

Run:

```bash
fab standalone.setup:query=queries/total_words.py,oids=$PWD/oids.txt
cd standalone
zip -r bluclobber.zip bluclobber/
nohup spark-submit --py-files bluclobber.zip query.py 144 > output_submission &
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
grep Exec output_submission | wc -l
```

---

## Troubleshooting: `ImportError: No module named api`

If, when running `fab` you see:

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

If when running `fab standalone` you get:

```bash
/bin/sh: pyspark: command not found
...
Aborting.
```

Then add Apache Spark to your `PATH`:

```bash
export PATH=~/spark-2.3.0-bin-hadoop2.7/bin:$PATH
```
