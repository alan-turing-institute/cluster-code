from pyspark import SparkContext, SparkConf  # pylint: disable=import-error
import requests

def get_streams(downsample=1, source="files.txt", app="Books", num_cores=1):

    conf = SparkConf()
    conf.setAppName(app)
    conf.set("spark.cores.max", num_cores)
    context = SparkContext(conf=conf)

    filenames = map(lambda x: x.strip(), list(open('files.txt')))

    are_urls = len(filenames) > 0 and \
        (filenames[0].lower().startswith("http://") or \
         filenames[0].lower().startswith("https://"))

    rdd_filenames = context.parallelize(filenames, num_cores)
#    down = rddfilenames.sample(False, 1.0 / downsample )
    down = rdd_filenames
    if (are_urls):
        streams = down.map(lambda x:
                           requests.get(x, stream=True).raw)
        return streams
    else:  # file paths
        streams = down.map(lambda x: open(x))
        return streams
