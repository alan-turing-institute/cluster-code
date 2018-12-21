"""
Fabric-compliant tasks to set up and run a Spark text-analysis
job using "spark-submit".
"""

from fabric.api import task, lcd, local

DEPLOY_DIR = "standalone"


@task
def setup():
    """
    Set up directory with Python files.
    """
    local('rm -rf ' + DEPLOY_DIR)
    local('mkdir -p ' + DEPLOY_DIR)
    with lcd(DEPLOY_DIR):  # pylint: disable=not-context-manager
        local('cp -r ../bluclobber .')
        local('find . -iname "*.pyc" -delete')
        local('find . -iname "__pycache__" -delete')


@task
def prepare(filenames="../files.txt", query="", datafile=""):
    """
    Set up directory with Python files, file with list of
    filenames, query file and datafile required by the
    query file.
    """
    setup()
    with lcd(DEPLOY_DIR):  # pylint: disable=not-context-manager
        local('cp ' + filenames + ' files.txt')
        local('cp ../' + query + ' ./bluclobber/query.py')
        if datafile != "":
            local('cp ../' + datafile + ' input.data')
        local('zip -r ./bluclobber.zip bluclobber')


@task
def submit(num_cores=1):
    """
    Submit the query to Spark.
    """
    with lcd(DEPLOY_DIR):  # pylint: disable=not-context-manager
        local('zip -r ./bluclobber.zip bluclobber')
        local("nohup spark-submit --py-files bluclobber.zip bluclobber/standalone_runner.py " + str(num_cores) + " > log.txt &")


@task
def pytest():
    """
    Run tests using py.test.
    """
    with lcd(DEPLOY_DIR):  # pylint: disable=not-context-manager
        local('py.test')
