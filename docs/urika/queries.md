# Run queries on Urika

## Specify data files to query

Populate `oids.txt` with the paths to the data files e.g.:

```bash
find /mnt/lustre/<your-urika-username>/dch -name "*.zip" > oids.txt
```

Check:

```bash
cat oids.txt
```

You should see the following (where `<HOME>` is the path to your home directory, where you mounted the data):

```
/mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip
/mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip
...
```

---

## Specify a subset of data files to query

For experimentation, you may find it useful to run queries across a subset of the data. For example you can hard-code the paths:

```
/mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/000001143_0_1-20pgs__560409_dat.zip
/mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/000000874_0_1-22pgs__570785_dat.zip
```

Alternatively, you can run `find` over a subset of the paths:

```bash
find /mnt/lustre/<your-urika-username>/dch/BritishLibraryBooks/1510_1699/ -name "*.zip" > oids.txt
```

---

## Run queries (general form)

Queries are run as follows, where `<QUERY>` is the name of a query.

Create job for Spark:

```bash
fab standalone.setup:query=queries/<QUERY>.py,oids=$PWD/oids.txt
cd standalone
zip -r bluclobber.zip bluclobber/
```

Submit job to Spark:

```bash
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
