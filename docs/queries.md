# Available queries

The available queries, which can be substituted into `<QUERY>`, include the fol
lowing:

## Total books

Run:

```bash
fab standalone.setup:query=queries/total_books.py,oids=$PWD/oids.txt
cd standalone
zip -r bluclobber.zip bluclobber/
spark-submit --py-files bluclobber.zip query.py
```

Expected results, `number_of_books`:

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` only: 2
* Query over `1510_1699/` only: `693`

The number of books should be equal to the number of ZIP files over which the query was run.

---

## Total words

Run:

```bash
fab standalone.setup:query=queries/total_words.py,oids=$PWD/oids.txt
cd standalone
zip -r bluclobber.zip bluclobber/
spark-submit --py-files bluclobber.zip query.py
```

Expected results, `[number_of_books, number_of_words]`:

* Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` only: `[2, 4372]`
* Query over `1510_1699/` only: `[693, 17479341]` TODO

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
