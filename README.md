# Enabling Complex Analysis of Large Scale Digital Collections

This repository contains code from the first phase of '[Enabling
Complex Analysis of Large Scale Digital Collections](http://figshare.com/articles/Enabling_Complex_Analysis_of_Large_Scale_Digital_Collections/1319482)',
a project funded by the [Jisc Research Data
Spring](http://opensource.org/licenses/MIT).

The core project team are:

* PI Melissa Terras (UCL)
* CI James Baker (British Library)
* CI David Beavan (UCL)
* CI James Hetherington (UCL)
* CI Martin Zaltz Austwick (UCL)

Associated researchers (without who research questions none of this
could have happened!) are:

* Oliver Duke-Williams (UCL)
* Will Finley (Sheffield)
* Helen O'Neill (UCL)
* Anne Welsh (UCL)

All code is available for use and reuse under a
[MIT Licence](http://opensource.org/licenses/MIT)

For more info on the project see the
[UCL DH](http://blogs.ucl.ac.uk/dh/2015/05/07/bluclobber-or-enabling-complex-analysis-of-large-scale-digital-collections/) and [British Library Digital Scholarship](http://britishlibrary.typepad.co.uk/digital-scholarship/) blogs.

---

## UCL users

### Beware: epcc-sparkrods branch

The `epcc-sparkrods` branch currently does not work for UCL systems. This is because the code was refactored so that `newsrods/sparkrods.py` no longer  constructs UCL-specific URLs by prefixing OIDS file entries with `http://arthur.rd.ucl.ac.uk/objects/`. It would be expected that infrastructure specific functions in `deploy/`, which construct the OIDS files do this. These functions need to be updated to support this.

---

## Standalone users

If you don't have access to UCL's resources, you can run queries on
your local machine.

## Local machine requirements

* Apache Spark
  - https://spark.apache.org
* Java 8
* Python 2.7/3.4

### To install on Mac OS X

```bash
brew install apache-spark
```

### To install on CentOS 7

Install Java 1.8:

```bash
yum install java-1.8.0-openjdk-devel
wget https://repo.anaconda.com/archive/Anaconda2-5.1.0-Linux-x86_64.sh
```

Install Anaconda 5.1 Python 2.7:

* See https://www.anaconda.com/download/

```bash
bash Anaconda2-5.1.0-Linux-x86_64.sh
nano anaconda2.sh
```

Add content:

```
export PATH=/home/centos/anaconda2/bin:$PATH
```

```bash
source anaconda2.sh
pip install -r requirements.txt
```

Install Apache Spark:

* See https://spark.apache.org/downloads.html
* See https://spark.apache.org/docs/latest/index.html

```bash
wget http://apache.mirror.anlx.net/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz.asc
wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz.md5
wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz.sha512
wget https://www.apache.org/dist/spark/KEYS
gpg --import KEYS
gpg --verify spark-2.3.0-bin-hadoop2.7.tgz.asc spark-2.3.0-bin-hadoop2.7.tgz
md5sum spark-2.3.0-bin-hadoop2.7.tgz
cat spark-2.3.0-bin-hadoop2.7.tgz.md5 
sha512sum spark-2.3.0-bin-hadoop2.7.tgz
cat spark-2.3.0-bin-hadoop2.7.tgz.sha512 
tar -xf spark-2.3.0-bin-hadoop2.7.tgz
cd spark-2.3.0-bin-hadoop2.7/
export PATH=~/spark-2.3.0-bin-hadoop2.7/bin:$PATH
```

---

## Running standalone

To run standalone, run:

```bash
fab standalone.setup:query=queries/mean_pages.py,oids=$PWD/oids.txt standalone.test
```

`fab` sets up a `standalone` directory with the following format:

* `bluclobber`: a copy of `bluclobber`.
* `query.py`: a copy of the `query` e.g. `queries/mean_pages.py`.
* `oids.txt`: a copy of `oids.txt`.

To only set up the `standalone` directory, run:

```bash
fab standalone.setup:query=queries/mean_pages.py,oids=$PWD/oids.txt
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

To view results, run:

```bash
cat standalone/result.yml 
```

If using the sample data in `oids.txt`, you should see:

```bash
[3, 504239]
```

To check whether the results of `mean_pages.py` are correct, unzip the
ZIP files specified in `oids.txt` within the same directory, such that
all their XML documents end up within the same `ALTO` subdirectory,
then, search for `<String>` elements across all the XML documents
e.g.

```bash
grep \<String ALTO/*.xml | wc -l
```

The total should match that returned by `mean_pages.py` e.g. 504239.

### Running unit tests

To run unit tests using `fab`, run:

```bash
fab standalone.setup:query=queries/mean_pages.py,oids=$PWD/oids.txt standalone.pytest
```

You should see:

```bash
============================= test session starts ==============================
platform linux2 -- Python 2.7.14, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
rootdir: /home/centos/cluster-code, inifile:
collected 11 items                                                             

bluclobber/test/test_archive.py ..                                       [ 18%]
bluclobber/test/test_book.py ........                                    [ 90%]
bluclobber/test/test_page.py .                                           [100%]

========================== 11 passed in 0.20 seconds ===========================
```

To run unit tests using `pytest`, run:

```bash
cd standalone
pytest
```

### Troubleshooting: `pyspark: command not found`

If you get:

```
$ fab bash
fab standalone.setup:query=queries/mean_pages.py,oids=$PWD/oids.txt standalone.test
...
[localhost] local: pyspark < newsrods/local_runner.py
/bin/sh: pyspark: command not found
...
Aborting.
```

Then add Apache Spark to your `PATH`:

```
export PATH=~/spark-2.3.0-bin-hadoop2.7/bin:$PATH
```

### Troubleshooting: `ImportError: No module named api`

If, when running `fab` you see:

```
ImportError: No module named api
```

Then check your version of `Fabric` e.g.

```
pip freeze | grep Fabric
```

It should be 1.x e.g. 1.14.0 and not 2.x. Fabric changed between
version 1 and 2. See

See [fabric](https://github.com/fabric/fabric/issues/1743) issue [no
module named fabric.api
#1743](https://github.com/fabric/fabric/issues/1743).

---
