from kafka import KafkaConsumer

consumer = KafkaConsumer('test_topic',bootstrap_servers='master:9092,worker1:9092,worker2:9092')

for message in consumer:
        print("Topic:{},Partition:{}, Offset:{}, Key:{}, Value:{}"
              .format(message.topic,message.partition,message.offset,message.key,message.value))
