'''
A runner to run the analysis directly.
'''

from bluclobber.sparkrods import get_streams
from bluclobber.query import do_query  # noqa # pylint: disable=all

from pyspark import SparkContext, SparkConf  # pylint: disable=import-error
import yaml
import sys

def main():
    '''
    Link the file loading with the query
    '''

    num_cores = 1
    if len(sys.argv) > 1:
        num_cores = sys.argv[1]
    conf = SparkConf()
    conf.setAppName("Books")
    conf.set("spark.cores.max", num_cores)
    context = SparkContext(conf=conf)
    log = context._jvm.org.apache.log4j.LogManager.getLogger(__name__)
    archives = get_streams(context, num_cores, source="files.txt")
    results = do_query(archives, 'input.data', log)

    with open('result.yml', 'w') as result_file:
        result_file.write(yaml.safe_dump(dict(results)))


if __name__ == "__main__":
    main()
