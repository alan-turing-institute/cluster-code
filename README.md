# British Library Books Data Analysis

This repository contains code to analyse British Library Books data provided by [Gale](https://www.gale.com). The data is available under an open, public domain, licence. See [Datasets for content mining](https://www.bl.uk/collection-guides/datasets-for-content-mining) and [BL Labs Flickr Data: Book data and tag history (Dec 2013 - Dec 2014)](https://figshare.com/articles/BL_Labs_Flickr_Data/1269249). For links to the data itself, see [Digitised Books largely from the 19th Century](https://data.bl.uk/digbks/).

The complete data consists of ~1TB of digitised versions of ~68,000 books from the 16th to the 19th centuries . The books have been scanned into a collection of XML documents. Each book has one XML document one per page plus one XML document for metadata about the book as a whole. The XML documents for each book are held within a compressed, ZIP, file. These ZIP files occupy ~224GB.

---

## Enabling Complex Analysis of Large Scale Digital Collections

This code has its origins in the first phase of '[Enabling Complex Analysis of Large Scale Digital Collections](http://figshare.com/articles/Enabling_Complex_Analysis_of_Large_Scale_Digital_Collections/1319482)', a project funded by the [Jisc Research Data Spring](http://opensource.org/licenses/MIT).

The core project team were:

* PI Melissa Terras (UCL)
* CI James Baker (British Library)
* CI David Beavan (UCL)
* CI James Hetherington (UCL)
* CI Martin Zaltz Austwick (UCL)

Associated researchers (without who research questions none of this could have happened!) were:

* Oliver Duke-Williams (UCL)
* Will Finley (Sheffield)
* Helen O'Neill (UCL)
* Anne Welsh (UCL)

For more info on the project see the [UCL DH](http://blogs.ucl.ac.uk/dh/2015/05/07/bluclobber-or-enabling-complex-analysis-of-large-scale-digital-collections/) and [British Library Digital Scholarship](http://britishlibrary.typepad.co.uk/digital-scholarship/) blogs.

---

## Analysing humanities data using Cray Urika-GX

The "epcc-sparkrods" branch contains a version of the code that has been updated and extended by Rosa Filgueira and Mike Jackson of [EPCC](https://www.epcc.ed.ac.uk) in their role as members of the [Research Engineering Group](https://www.turing.ac.uk/research/research-engineering) of the [The Alan Turing Institute](https://www.turing.ac.uk).

This work was done in conjunction with Melissa Terras, College of Arts, Humanities and Social Sciences (CAHSS), The University of Edinburgh. This work looked at running the code on the [Alan Turing Institute Cray Urika-GX Service](https://ati-rescomp-service-docs.readthedocs.io/en/latest/cray/introduction.html).

This work was funded by Scottish Enterprise as part of the Alan Turing Institute-Scottish Enterprise Data Engineering Program.

### Use

* [Set up a local environment](./docs/setup-local.md)
* [Set up Urika environment](./docs/setup-urika.md)
* [Run queries](./docs/queries.md)
* [Run tests](./docs/tests.md)

**Note:** the `epcc-sparkrods` branch currently will not work on UCL systems. This is because the code was refactored so that `bluclobber/sparkrods.py` no longer constructs UCL-specific URLs by prefixing file names with `http://arthur.rd.ucl.ac.uk/objects/`. It would be expected that infrastructure specific functions in `deploy/`, which construct the file with filenames, default `files.txt`, will do this. These functions need to be updated to support this.

---

## Copyright and licence

Copyright (c) 2015 University College London

Copyright (c) 2018 The University of Edinburgh

All code is available for use and reuse under a [MIT Licence](http://opensource.org/licenses/MIT). See [LICENSE](./LICENSE).

### Data

The file:

bluclobber/test/fixtures/000000037_0_1-42pgs__944211_dat_modified.zip

is a modified copy of the file 000000037_0_1-42pgs__944211_dat.zip from [OCR text derived from digitised books published 1880 - 1889 in ALTO XML](https://data.bl.uk/digbks/db11.html) (doi: 10.21250/db11) which is licenced under [CC0 1.0 Public Domain](https://creativecommons.org/licenses/by/4.0/).

The modifications are as follows.

000000037_metadata.xml:

```
-               <MODS:placeTerm type="text">Manchester</MODS:placeTerm>
=>
+               <MODS:placeTerm type="text">Manchester [1823]</MODS:placeTerm>
```

000000218_metadata.xml:

```
-               <MODS:placeTerm type="text">London</MODS:placeTerm>
+               <MODS:placeTerm type="text">London [1823]</MODS:placeTerm>
```
