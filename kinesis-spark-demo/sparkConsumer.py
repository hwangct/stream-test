from __future__ import print_function

import sys
#import boto
import json

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream

if __name__ == "__main__":
        # initialize input
        appName = "PythonStreamingToS3Example"
        streamName = "kinesis-demo"
        endpointUrl = "kinesis.us-east-1.amazonaws.com"
        regionName = "us-east-1"
        sc = SparkContext(appName=appName)
        # batch duration set to 1 millisecond
        ssc = StreamingContext(sc, 1)
        lines = KinesisUtils.createStream(
            ssc, appName, streamName, endpointUrl, regionName, InitialPositionInStream.LATEST, 2)
        counts = lines.flatMap(lambda line: line.split(" ")) \
            .map(lambda word: (word, 1)) \
            .reduceByKey(lambda a, b: a+b)
        counts.print()

        ssc.start()
        ssc.awaitTermination()

        # S3 API
        # data = {"Writing some sample data": []}
        # s3 = boto3.resource('s3')

        # Put s3 object in bucket
        # obj = s3.Object('kinesis-spark-bucket','kinesis-spark.json')
        # obj.put(Body=json.dumps(data))

    # if len(sys.argv) != 5:
    #         print(
    #             "Usage: kinesis_wordcount_asl.py <app-name> <stream-name> <endpoint-url> <region-name>",
    #             file=sys.stderr)
    #         sys.exit(-1)

    #     sc = SparkContext(appName="PythonStreamingKinesisWordCountAsl")
    #     ssc = StreamingContext(sc, 1)
    #     appName, streamName, endpointUrl, regionName = sys.argv[1:]
    #     lines = KinesisUtils.createStream(
    #         ssc, appName, streamName, endpointUrl, regionName, InitialPositionInStream.LATEST, 2)
    #     counts = lines.flatMap(lambda line: line.split(" ")) \
    #         .map(lambda word: (word, 1)) \
    #         .reduceByKey(lambda a, b: a+b)
    #     counts.print()

    #     ssc.start()
    #     ssc.awaitTermination()