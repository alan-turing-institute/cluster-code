import pyspark
import requests

def get_streams(downsample=1, source="oids.txt", app="Books"):


    sc = pyspark.SparkContext(appName=app)

    oids = map(lambda x: x.strip(), list(open('oids.txt')))

    rddoids = sc.parallelize(oids)
#    down = rddoids.sample(False, 1.0 / downsample )
    down = rddoids
    streams = down.map(lambda x:
                       requests.get(x, stream=True).raw)
    return streams
