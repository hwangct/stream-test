# Sample pyspark code with dictionaries
dict0 = {'fname':'Jeff', 'lname':'Aven', 'pos':'author'}
dict1 = {'fname':'Barack', 'lname':'Obama', 'pos':'president'}
dict2 = {'fname':'Ronald', 'lname':'Reagan', 'pos':'president'}
dict3 = {'fname':'John', 'mi':'F', 'lname':'Kennedy', 'pos':'president'}
dict4 = {'fname':'Jeff', 'lname':'Aven', 'pos':'author'}

people = sc.parallelize([dict0, dict1, dict2, dict3])
presidents = people.filter(lambda x: x['pos'] == 'president') \
                .map(lambda x: x['fname'] + " " + x['lname'])

# Sample pyspark code with tuples
tempc = sc.parallelize([38.4, 19.2, 12.8, 9.6])
temp_tups = tempc.map(lambda x: (x,(float(9)/5)*x + 32))

# Sample pyspark code with sets
tempc = sc.parallelize(set([38.4, 19.2, 12.8, 9.6]))

# Sample pyspark code with lists
tempc = sc.parallelize([38.4, 19.2, 12.8, 9.6])
tempf = tempc.map(lambda x: (float(9)/5)*x + 32)

# Sample pyspark code with JSON
json_str = '''{
    "people" : [
        {"fname": "Jeff",
        "lname": "Aven",
        "tags": ["big data","hadoop"]},
        {"fname": "Doug",
        "lname": "Cutting",
        "tags": ["hadoop","avro","apache","java"]},
        {"fname": "Martin",
        "lname": "Odersky",
        "tags": ["scala","typesafe","java"]},
        {"fname": "John",
        "lname": "Doe",
        "tags": []}
        ]}'''
people_obj = json.loads(json_str)
people = sc.parallelize(people_obj["people"])
hadoop_tags = people.filter(lambda x: "hadoop" in x['tags']) \
            .map(lambda x: x['fname'] + " " + x['lname'])

# Pyspark API sample()
logs = sc.textFile('file:///path/to/logs')
logs.sample(False, 0.1, seed=None) - create a sampled subset based on percentage of the overall

# Pyspark API takeSample()
dataset = sc.parallelize([1,2,3,4,5,6,7,8,9,10])
dataset.takeSample(False, 3)

# Pyspark API map() evaulates a named or anonymous functin for each element within a partition of a dataset
Pyspark API flatMap() is the same as map(), but removes a level of nesting to produce a single list
Pyspark API filter() transformation evaluates a Boolean expresssion against each element to remove records do not return True

# Pyspark API groupBy() returns an RDD of items grouped by a specified function
# Pyspark API sortBy() sorts an RDD by the function that nominates the key for a given dataset.
# Pyspark API distinct() returns a new RDD containing distinct elements and removes duplicates.
logs = sc.textFile('file:///path/to/logs')
logrecs = logs.map(lambda x: x.split(' '))
reqfieldsonly = logrecs.map(lambda x: (x[7], x[11]))
distinctrecs = reqfieldsonly.distinct()
sorted = distinctrecs.sortBy(lambda x: x[1]) \
            .map(lambda x: (x[1], x[0]))
grouped = sorted.groupBy(lambda x: x[0]) \
            .map(lambda x: (x[0], list(x[1])))

# Pyspark API union() takes one RDD and appends another RDD to it
odds = sc.parallelize([1,3,5,7,9])
fibonacci = sc.parallelize([0,1,2,3,5,8])
odds.union(fibonacci).collect()

# Pyspark API intersection() returns elements that are present in both RDDs
odds = sc.parallelize([1,3,5,7,9])
fibonacci = sc.parallelize([0,1,2,3,5,8])
odds.intersection(fibonacci).collect()

# Pyspark API subtract() returns all elements from the first RDD that are not present in the second RDDs
odds = sc.parallelize([1,3,5,7,9])
fibonacci = sc.parallelize([0,1,2,3,5,8])
odds.subtract(fibonacci).collect()

# Psypark API count() action returns the number of elements or records in an RDDs
lorem = sc.textFile('file:///path/to/file')
words = lorem.flatMap(lambda x: x.split())
words.count()

# Psypark API collect() action returns a list that contains all of the elements in an RDD to the Spark driver
lorem = sc.textFile('file:///path/to/file')
words = lorem.flatMap(lambda x: x.split())
words.collect()

# Pyspark API take() returns the first n elements of an RDD
lorem = sc.textFile('file:///path/to/file')
words = lorem.flatMap(lambda x: x.split())
words.take(3)

# Pyspark API top() returns the top n elements from an RDD, ordered and returned in descending order
lorem = sc.textFile('file:///path/to/file')
words = lorem.flatMap(lambda x: x.split())
words.top(3)

# Pyspark API first() returns the first element in this RDD
lorem = sc.textFile('file:///path/to/file')
words = lorem.flatMap(lambda x: x.split())
words.first()

# Pyspark API reduce() reduces the elements using a specified commutative and associative operator.
numbers = sc.parallelize([1,2,3,4,5,6,7,8,9])
numbers.reduce(lambda x, y: x + y)

# Pyspark API fold() aggregrates the elements of each partition of an RDD, then perform the aggregate operatoin against the
# results for all using a given associative and commutative function and a zeroValue.  
empty = sc.parallelize([])
empty.reduce(lambda x, y: x + y)
# ValueError: Can not reduce() empty RDD
empty.fold(0, lambda x, y: x + y)
# 0

# Pyspark API foreach() applies a function to all elements of an RDD.  
def printfunc(x): print(x)
lorem = sc.textFile('file:///path/to/file')
words = lorem.flatMap(lambda x: x.split())
words.foreach(lambda x: printfunc(x))