from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
#from pyspark.sql.functions import from_json
from pyspark.sql import functions as func
from pyspark.sql.types import StructType, StringType


spark = SparkSession.builder.appName("testConsumer").getOrCreate()

#spark.sparkContext.setLogLevel('WARN')

df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "master:9092")\
    .option("subscribe","test2").load()

aa = df.selectExpr("CAST (value AS STRING)")

bb = aa.withColumn("eventTime",func.current_timestamp())

cc = bb.groupBy(func.window(func.col("eventTime"),"30 seconds", "10 seconds"),func.col("value")).count()

dd = cc.orderBy(func.col("count").desc())

query = dd.writeStream.outputMode("complete").format("console").start()

query.awaitTermination()

spark.stop()
