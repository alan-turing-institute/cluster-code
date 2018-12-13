# Set up local environment

## Requirements

* Apache Spark
  - https://spark.apache.org
* Java 8
* Python 2.7/3.4

## Install on Mac OS X

```bash
brew install apache-spark
```

## Install on CentOS 7

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

```bash
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
