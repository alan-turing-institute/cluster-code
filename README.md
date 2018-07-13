# Enabling Complex Analysis of Large Scale Digital Collections

This repository contains code from the first phase of '[Enabling Complex Analysis of Large Scale Digital Collections](http://figshare.com/articles/Enabling_Complex_Analysis_of_Large_Scale_Digital_Collections/1319482)', a project funded by the [Jisc Research Data Spring](http://opensource.org/licenses/MIT).

The core project team are:

- PI Melissa Terras (UCL)
- CI James Baker (British Library)
- CI David Beavan (UCL)
- CI James Hetherington (UCL)
- CI Martin Zaltz Austwick (UCL)

Associated researchers (without who research questions none of this could have happened!) are:
- Oliver Duke-Williams (UCL)
- Will Finley (Sheffield)
- Helen O'Neill (UCL)
- Anne Welsh (UCL)

All code is available for use and reuse under a [MIT Licence](http://opensource.org/licenses/MIT)

For more info on the project see the [UCL DH](http://blogs.ucl.ac.uk/dh/2015/05/07/bluclobber-or-enabling-complex-analysis-of-large-scale-digital-collections/) and [British Library Digital Scholarship](http://britishlibrary.typepad.co.uk/digital-scholarship/) blogs.

---

## UCL users

### Beware: epcc-master branch

The `epcc-master` branch has not been tested on UCL systems. 

---

## Urika users

### Set up Python environment

Create `py27` environment:

```bash
module load anaconda3/4.1.1
conda create -n py27 python=2.7 anaconda

Proceed ([y]/n)? y
```

Activate environment:

```bash
source activate py27
```

Show active environment:

```bash
conda env list
```
```
# conda environments:
#
py27                  *  /home/users/michaelj/.conda/envs/py27
root                     /opt/cray/anaconda3/4.1.1
```

Install dependencies:

```bash
cd cluster-code
conda install -c anaconda --file requirements.txt
```

**Note**:  After creating the `py27` environment, for your subsequent Urika sessions you just need to type:

```bash
module load anaconda3/4.1.1
source activate py27
```

### Load additional modules

Load `mrun` module:

```
module load mrun
```

### Mount data using SSHFS

```bash
mkdir blpaper
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-uun>@chss.datastore.ed.ac.uk:/chss/datastore/chss/groups/Digital-Cultural-Heritage dch
```

Create data directory on Lustre:

```
mkdir -P /mnt/lustre/<your-uun>/dch
```

Copy data files into `lustre` file system:

```
source deploy/bl_copy.sh ~/dch/BritishLibraryBooks/ /mnt/lustre/<your-uun>/dch/BritishLibraryBooks
```

This may take some time.

Alternatively, use `<your-urika-username>` instead of `<your-uun>`.

**Important note:**

* Do **not** mount the DataStore directory directly onto Lustre. Urika compute nodes have no network access and so can't access DataStore via the mount. Also, for efficient processing, data movement needs to be minimised. Copy the data into Lustre as above.

### Update execution script

Change urika.sh to specify the path to your files e.g.:

```
remote_directory='/mnt/lustre/<your-uun>/dch/BritishLibraryBooks'
```

### Run normaliser query

Run:

```
fab urika.setup:query=queries/normaliser.py urika.run:query_name=normaliser
```

This will process the data, using MPI, as background processes.

To check if the processing has completed, inspect the `output_submission` log file:

```
tail production/bluclobber/harness/output_submission
```

You should see:

```
+ python result_normaliser.py ./output_normaliser/ ./data_normaliser/
```

If processing is still ongoing, running

```
ps
```

will show `urika.sh` as a running process:

```
   PID TTY          TIME CMD
135097 pts/0    00:00:00 urika.sh
```

Copy `data_normaliser/normaliser.yml`, and other outputs, before running another query. This file is needed for visualising results. `production/` will be deleted and recreated when running subsequent queries.

```
mkdir results
cp -r production/bluclobber/harness/data_normaliser/ results/
cp -r production/bluclobber/harness/output_normaliser/ results/
cp production/bluclobber/harness/output_submission results/output_submission_normaliser.txt
```

### Check normaliser query resuults

As a quick and dirty check, run:

```
wc production/bluclobber/harness/data_normaliser/normaliser.yml
```

You should see:

```
287 1148 7780 production/bluclobber/harness/data_normaliser/normaliser.yml
```

Run:

```
head production/bluclobber/harness/data_normaliser/normaliser.yml
```

You should see:

```
1788:  [102, 22588, 4055011]
1789:  [46, 8704, 2189602]
1853:  [593, 241076, 77715088]
1780:  [28, 3387, 764487]
1781:  [29, 5442, 1265452]
1782:  [23, 3290, 573673]
1783:  [23, 2704, 438293]
1784:  [22, 2626, 1276893]
1785:  [43, 10245, 2894281]
1786:  [34, 2624, 442562]
```

### Run diseases query

Run:

```
fab urika.setup:query=queries/normaliser.py urika.run:query_name=diseases
```

This will process the data, using MPI, as background processes.

To check if the processing has completed, inspect the `output_submission` log file:

```
tail production/bluclobber/harness/output_submission
```

You should see:

```
dissease diarrhoea: {1824: 2, 1860: 2, 1862: 36, 1888: 1, 1867: 2, 1868: 1, 1807: 1, 1880: 1, 1881: 2, 1882: 1, 1819: 2, 1822: 1, 1760: 1, 1890: 1, 1894: 1, 1895: 2, 1832: 2, 1852: 1, 1898: 2, 1835: 1, 1839: 59, 1896: 2, 1843: 1, 1844: 1, 1886: 1, 1777: 1, 1788: 1}

wrote
```

If processing is still ongoing, running

```
ps
```

will show `urika.sh` as a running process:

```
   PID TTY          TIME CMD
135097 pts/0    00:00:00 urika.sh
```

Copy `data_diseases/*.yml`, and other outputs, before running another query. This file is needed for visualising results. `production/` will be deleted and recreated when running subsequent queries.

```
cp -r production/bluclobber/harness/data_diseases/ results/
cp -r production/bluclobber/harness/output_diseases/ results/
cp production/bluclobber/harness/output_submission results/output_submission_diseases.txt
```

### Notes

16 nodes are used, as specified in urika.sh. The code does not sale beyond that

`bluclubber/harness/join_*py` merges files from each process, but can end up with duplicated keys.

`bluclobber/harness/result_diseases.py` creates a single file for each type of disease.

`bluclobber/harness/result_normalize.py` creates a single file with one key per year.
