import sys
import os
import shutil
import glob
import yaml

path=sys.argv[1]
joined_files = sorted([f for f in glob.glob(path+'/out*')])
year_data = {}
outfilename=path+"/total.yml"
for f in joined_files:
    with open(f, 'r') as stream:
        with open(outfilename, 'a+') as outfile:
            shutil.copyfileobj(stream, outfile)

