# British Library Books Data Analysis

This repository contains code to analyse British Library Books data provided by [Gale](https://www.gale.com). The data is available under an open, public domain, licence. See [Datasets for content mining](https://www.bl.uk/collection-guides/datasets-for-content-mining) and [BL Labs Flickr Data: Book data and tag history (Dec 2013 - Dec 2014)](https://figshare.com/articles/BL_Labs_Flickr_Data/1269249)

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

Using a local machine:

* [Set up a local environment](./docs/local/setup.md)
* [Run queries locally](./docs/local/queries.md)
* [Run tests locally](./docs/local/tests.md)

Using Urika:

* [Set up Urika environment](./docs/urika/setup.md)
* [Run queries on Urika](./docs/urika/queries.md)
* [Run tests on Urika](./docs/urika/tests.md)

Both:

* [Available queries](./docs/queries.md)

**Note:** the `epcc-sparkrods` branch currently will not work on UCL systems. This is because the code was refactored so that `bluclobber/sparkrods.py` no longer constructs UCL-specific URLs by prefixing OIDS file entries with `http://arthur.rd.ucl.ac.uk/objects/`. It would be expected that infrastructure specific functions in `deploy/`, which construct the OIDS files do this. These functions need to be updated to support this.

---

## Copyright and licence

Copyright (c) 2015 University College London

Copyright (c) 2018 The University of Edinburgh

All code is available for use and reuse under a [MIT Licence](http://opensource.org/licenses/MIT). See [LICENSE](./LICENSE).
