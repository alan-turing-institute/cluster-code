# Available queries

The available queries, which can be substituted into `<QUERY>`, include the fol
lowing:

## Total books

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

---

## Total words

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

## Check the number of executors used

A quick-and-dirty way to get this number is to run:

```bash
grep Exec output_submission | wc -l
```
