'''
Fab file for deployment.
'''

from deploy.remote import *
from deploy.grace import *
from deploy import standalone

# deploy.remote configuration.
env.user='ucgajhe'
env.results_dir="/home/"+env.user+"/Scratch/BluclobberSpark/output"
env.model="bluclobber"
env.corpus='/rdZone/live/rd003v/CompressedALTO-fromJamesH/CompressedALTO'
env.deploy_to="/home/"+env.user+"/devel/BluclobberSpark"

# deploy.standalone configuration.
env.standalone_deploy_dir = 'standalone'
