from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['master:9092', 'worker1:9092', 'worker2:9092'])

for i in range(0,10):
  data = {}.format(i)
  producer.send('test_topic', data.encode())
