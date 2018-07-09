import pyspark
import requests

def get_streams(downsample=1, source="oids.txt", app="Books"):


    sc = pyspark.SparkContext(appName=app)

    oids = map(lambda x: x.strip(), list(open('oids.txt')))

    are_urls = len(oids) > 0 and \
        (oids[0].lower().startswith("http://") or \
         oids[0].lower().startswith("https://"))

    rddoids = sc.parallelize(oids)
#    down = rddoids.sample(False, 1.0 / downsample )
    down = rddoids
    if (are_urls):
        streams = down.map(lambda x:
                           requests.get(x, stream=True).raw)
        return streams
    else:  # file paths
        streams = down.map(lambda x: open(x))
        return streams
