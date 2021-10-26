from kafka import KafkaProducer
import csv

producer = KafkaProducer(bootstrap_servers=['master:9092', 'worker1:9092', 'worker2:9092'])

f=open('/home/gwangil/SmartCarStatusInfo_20211022.csv','r',)

lines=f.readlines()
for line in lines:
	producer.send('test', line.strip().encode())
