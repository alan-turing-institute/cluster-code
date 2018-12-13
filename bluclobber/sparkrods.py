from pyspark import SparkContext, SparkConf  # pylint: disable=import-error
import requests

def get_streams(downsample=1, source="oids.txt", app="Books", num_cores=1):

    conf = SparkConf()
    conf.setAppName(app)
    conf.set("spark.cores.max", num_cores)
    context = SparkContext(conf=conf)

    oids = map(lambda x: x.strip(), list(open('oids.txt')))

    are_urls = len(oids) > 0 and \
        (oids[0].lower().startswith("http://") or \
         oids[0].lower().startswith("https://"))

    rddoids = context.parallelize(oids, num_cores)
#    down = rddoids.sample(False, 1.0 / downsample )
    down = rddoids
    if (are_urls):
        streams = down.map(lambda x:
                           requests.get(x, stream=True).raw)
        return streams
    else:  # file paths
        streams = down.map(lambda x: open(x))
        return streams
