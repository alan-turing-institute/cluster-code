# Set up Urika environment

## Set up Python environment

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
py27                  *  /home/users/<your-urika-username>/.conda/envs/py27
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

## Mount data using SSHFS

```bash
mkdir dch
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-urika-username>@chss.datastore.ed.ac.uk:<path-in-uoe-datastore> dch
```

Create data directory on Lustre:

```bash
mkdir -p /mnt/lustre/<your-urika-username>/dch
```

Copy the complete data set to Lustre, by running in your home directory:

```bash
source deploy/bl_copy.sh ~/dch/BritishLibraryBooks/ /mnt/lustre/<username>/dch/BritishLibraryBooks
```

**Important note:**

* Do **not** mount the DataStore directory directly onto Lustre. Urika compute nodes have no network access and so can't access DataStore via the mount. Also, for efficient processing, data movement needs to be minimised. Copy the data into Lustre as above.

Set data file permissions:

```bash
chmod -R u+rx /mnt/lustre/<your-urika-username>/dch/*/*.zip
```
