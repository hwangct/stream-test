import re
from pyspark import SparkContext

sc = SparkContext(appName="PythonWordCount")
doc = sc.textFile("file:///opt/spark/data/streaming/shakespeare.txt")

flattened = doc.filter(lambda line: len(line) > 0) \
.flatMap(lambda line: re.split('\W+', line))

kvpairs = flattened.filter(lambda word: len(word) > 0) \
 .map(lambda word:(word.lower(),1))

# repartition into 5 partitions
countsbyword = kvpairs.reduceByKey(lambda v1, v2: v1 + v2, \
numPartitions=5)

topwords = countsbyword.map(lambda (w, c): (c, w)) \
.sortByKey(ascending=False)

topwords.saveAsTextFile("file:///opt/spark/data/streaming/wordcounts")