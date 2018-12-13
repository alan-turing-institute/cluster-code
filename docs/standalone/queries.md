# Run queries standalone

## Specify data files to query

Populate `oids.txt` with the paths to the data files e.g.:

```bash
find $HOME/dch -name "*.zip" > oids.txt
```

Check:

```bash
cat oids.txt
```

You should see the following (where `<HOME>` is the path to your home directory, where you mounted the data):

```
<HOME>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip
<HOME>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip
...
```

---

## Specify a subset of data files to query

For experimentation, you may find it useful to run queries across a subset of the data. For example (where `<HOME>` is the path to your home directory, where you mounted the data) you can hard-code the paths:

```
<HOME>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip
<HOME>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip
```

Alternatively, you can run `find` over a subset of the paths:

```bash
find $HOME/dch/BritishLibraryBooks/1510_1699/ -name "*.zip" > oids.txt
```

---

## Run queries (general form)

Queries are run as follows, where `<QUERY>` is the name of a query:

```bash
fab standalone.setup:query=queries/<QUERY>.py,oids=$PWD/oids.txt standalone.test
```

`fab` sets up a `standalone` directory with the following format:

* `bluclobber`: a copy of `bluclobber`.
* `query.py`: a copy of the `query` i.e. `queries/<QUERY>.py`.
* `oids.txt`: a copy of `oids.txt`.

To set up the `standalone` directory, without running the query, run:

```bash
fab standalone.setup:query=queries/<QUERY>.py,oids=$PWD/oids.txt
```

To run using `pyspark`, run:

```bash
cd standalone
pyspark < query.py
```

To run using `spark-submit`, run:

```bash
cd standalone
zip -r bluclobber.zip bluclobber/
spark-submit --py-files bluclobber.zip query.py
```

Check results:

```bash
cat result.yml 
```

See [Available queries](../queries.md) for available queries, which can be substituted into `<QUERY>`.

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
fab standalone.setup:query=queries/total_words.py,oids=$PWD/oids.txt standalone.test
...
/bin/sh: pyspark: command not found
...
Aborting.
```

Then add Apache Spark to your `PATH`:

```bash
export PATH=~/spark-2.3.0-bin-hadoop2.7/bin:$PATH
```
