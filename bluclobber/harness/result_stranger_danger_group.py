import sys
import os
import shutil
import glob
import yaml

inputpath=sys.argv[1]
outputpath=sys.argv[2]
joinfilename=inputpath+"/total.yml"
finalfilename=outputpath+"/final.yml"


with open(joinfilename,'r') as fin:
    with open(finalfilename, "wt") as fout:
        for line in fin:
            fout.write(line.replace('? [stranger, danger]', ''))

with open(finalfilename,'r+') as file:
  filedata = file.read()

filedata = filedata.replace(': - -', '  - - ')

with open(finalfilename, 'w') as file:
  file.write(filedata)

with open(finalfilename,'r+') as fh:
    lines = fh.readlines()
    fh.seek(0)
    lines.insert(0, '(stranger, danger):')
    fh.writelines(lines)
          

