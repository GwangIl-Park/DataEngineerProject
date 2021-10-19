from kafka import KafkaProducer
import datetime
import string
from random import randint

producer = KafkaProducer(bootstrap_servers=['master:9092', 'worker1:9092', 'worker2:9092'])

for i in range(0,10):
  alphabet_list = list(string.ascii_uppercase)

  car_number = alphabet_list[randint(0,len(alphabet_list)-1)] + '{0:04d}'.format(randint(0,9999))
  str_msg=''
  str_msg+= datetime.datetime.now().strftime("%Y%m%d%H%m")+','
  str_msg+= car_number+','
  for i in range(0,4):
    a = randint(0,100) + 60
    if a > 100:
      a = 100
    str_msg+=str(a)+','
  for i in range(0,4):
    a = randint(0,100)
    if a == 1:
      str_msg+='2,'
    else:
      str_msg+='1,'
  for i in range(0,2):
    a = randint(0,100)
    if a==1:
      str_msg+='C,'
    elif 2 < a and a < 6:
      str_msg+='B,'
    else:
      str_msg+='A,'
  str_msg+=str(randint(1,100))+','
  str_msg+='20211001'

  response = producer.send('test_topic', str_msg.encode()).get()
  print(response)