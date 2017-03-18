from pyspark import SparkConf, SparkContext
import csv
conf = (SparkConf()
         .setMaster("local")
         .setAppName("tp")
         .set("spark.executor.memory", "1g"))
sc = SparkContext(conf = conf)

#working1
# ds_real =sc.textFile("/home/chai/Desktop/BDA/test.csv") \
#     .map(lambda line: line.split(",")) \
#     .filter(lambda line: len(line)>1) \
#     .map(lambda line: (line[0],line[1])) \
#     .collect()
# ds_real = sc.parallelize(ds_real)

#working2
#ds_real = sc.parallelize([("Barrister Rajni Patel Marg",375000),("HDIL Building, Sahar Road, Andheri East, Mumbai",1000),("Abc",200)])
for i in range(0,15):
	ds_real = sc.textFile("/home/chai/Desktop/BDA/cluster"+str(i)+".csv")
	ds_real = ds_real.mapPartitions(lambda x: csv.reader(x))


	total = (ds_real.map(lambda (location, price): price)).reduce(lambda x,y:int(x)+int(y))
	num = ds_real.count()
	average = total / num
	print "cluster"+str(i)
	print (average)
	print "\n"
#print ()