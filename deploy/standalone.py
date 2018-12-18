'''
Set up to run standalone without use of IRODS.
'''

import os
import pandas as pd
from fabric.api import task, env, execute, lcd, local


@task
def setup(query, filenames):
    '''
    Prepare instance for running. Generates necessary files.
    '''
    execute(install, query=query, filenames=filenames)


@task
def install(query, filenames):
    '''
    Generate necessary files.
    '''
    local('rm -rf ' + env.standalone_deploy_dir)
    local('mkdir -p ' + env.standalone_deploy_dir)
    with lcd(env.standalone_deploy_dir):  # pylint: disable=not-context-manager
        local('cp -r ../bluclobber .')
        local('cp ../' + query + ' ./query.py')
        local('cp ' + filenames + ' files.txt')
        local('find . -iname "*.pyc" -delete')
        local('find . -iname "__pycache__" -delete')


@task
def test():
    '''
    Run the query.
    '''
    with lcd(env.standalone_deploy_dir):  # pylint: disable=not-context-manager
        local('pyspark < query.py')


@task
def pytest():
    '''
    Run pytest tests.
    '''
    with lcd(env.standalone_deploy_dir):  # pylint: disable=not-context-manager
        local('py.test')
