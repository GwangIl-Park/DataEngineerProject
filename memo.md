<h1> 2021-10-13 </h1>

<h3> 리눅스 환경 설정 </h3>

centos7 사용

virtual box 네트워크에 NAT네트워크, 호스트전용 어댑터 설정

yum update

yum upgrade

yum install openssh

yum install net-tools

* centos설치후 인터넷 연결 안됐을 때

nmcli d 로 이더넷 카드 확인 후 disconnected이면

nmtui를 통해 연결해주자

<h1> 2021-10-14 </h1>

<h3> 리눅스 환경설정 이어서.. + 하둡, 주키퍼 등 설치</h3>

https://earthconquest.tistory.com/235 블로그 참고

* 자바 설치

yum list -installed java* 또는 rpa -qa | grep java로 기존에 설치된 자바 패키지가 있다면 "yum remove 패키지명" 으로 삭제

자바 설치 후, 심볼릭 링크 지정 -> ln -s jdk1.8.0_291/ java

/etc/profile에 환경변수 추가

export JAVA_HOME=/usr/local/java  
export PATH=$PATH:$JAVA_HOME/bin  
export CLASSPATH="."

이후 java -version으로 확인

* 방화벽 중지

systemctl stop firewalld  
systemctl disable firewalld  
firewall-cmd --state

/etc/hostname 에 hostname 지정 -> master, worker1, worker2로 했음

/etc/hosts에 ip, 도메인, 호스트 추가

127.0.0.1   localhost master

192.168.56.107 master.com master  
192.168.56.110 worker1.com worker1  
192.168.56.111 worker2.com worker2  

/etc/sysconfig/network에 도메인명 추가

NETWORKING=yes
NETWORKING IPV6=no
HOSTNAME=hadoop01.com

/etc/selinux/config에서 SELINUX=disabled로 수정

스왑 메모리 추가

sysctl -w vm.swappiness=100

/etc/sysctl.conf 에 vm.swappiness=100 추가

/etc/rc.local 에 다음과 같이 추가

echo never > /sys/kernel/mm/transparent_hugepage/enabled  
echo never > /sys/kernel/mm/transparent_hugepage/defrag

/etc/security/limits.conf 에 파일 디스크립터 설정 추가

root soft nofile 65536  
root hard nofile 65536  
* soft nofile 65536  
* hadr nofile 65536  
root soft nproc 32768  
root hard nproc 32768  
* soft nproc 32768  
* hard nproc 32768

* ssh키 생성 및 복제

ssh-keygen -t rsa

ssh-copy-id -i /home/gwangil/.ssh/id_rsa.pub gwangil@master

ssh-copy-id -i /home/gwangil/.ssh/id_rsa.pub gwangil@worker1

ssh-copy-id -i /home/gwangil/.ssh/id_rsa.pub gwangil@worker2

* protobuf 설치 : 직렬화 라이브러리, 서버간 데이터 통신 또는 다른 종류의 언어로 개발된 통신을 바이너리 데이터로 전송해줌

su - root  
cd /usr/local  
wget https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.gz  
tar xvfz protobuf-2.5.0.tar.gz  
cd protobuf-2.5.0  
./configure  
make  
make install

* 나는 gcc 설치가 안돼서 빌드가 안됐음 다음을 설치

yum install gcc glibc glibc-common gd gd-devel -y

yum install gcc-c++

* zookeeper 설치

zookeeper 유저 추가 후, slave 서버에 전달

주키퍼 설치

wget https://mirror.navercorp.com/apache/zookeeper/zookeeper-3.6.3/apache-zookeeper-3.6.3-bin.tar.gz

tar xvfz apache-zookeeper-3.6.3-bin.tar.gz 

zoo.cfg에 다음 내용 변경

dataDir=/home/zookeeper/apache-zookeeper-3.6.3-bin/data

server.1=0.0.0.0:2888:3888  -> 자기 자신의 host를 인식 못하는 경우가 있는데 0.0.0.0으로 하면 된다고 함
server.2=worker1:2888:3888  
server.3=worker2:2888:3888

dataDir 경로에 myid 추가하고 위 server설정에 해당하는 숫자를 넣고 저장 (master의 경우 1)

bashrc에 alias 추가

alias zoo-start="/home/zookeeper/apache-zookeeper-3.6.3-bin/bin/zkServer.sh start"  
alias zoo-status="/home/zookeeper/apache-zookeeper-3.6.3-bin/bin/zkServer.sh status"  
alias zoo-stop="/home/zookeeper/apache-zookeeper-3.6.3-bin/bin/zkServer.sh stop"

source $HOME/.bashrc

환경 변수 추가

export ZOOKEEPER_HOME=/home/zookeeper/apache-zookeeper-3.6.3-bin

PATH=$PATH:$HOME/.local/bin:$HOME/bin:$ZOOKEEPER_HOME/bin

export PATH

zoo-status해보면 하나가 leader로 선출된것 볼수 있음

<h1> 2021-10-15 </h1>

<h3> 하둡 설치 </h3>

wget http://apache.mirror.cdnetworks.com/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz

tar -xvzf hadoop-3.3.0.tar.gz

ln -s hadoop-3.3.0 hadoop

* 환경변수 설정

export JAVA_HOME=/usr/local/java  
export HADOOP_HOME=/home/gwangil/hadoop  
export HADOOP_INSTALL=$HADOOP_HOME  
export HADOOP_MAPRED_HOME=$HADOOP_HOME  
export HADOOP_COMMON_HOME=$HADOOP_HOME  
export HADOOP_HDFS_HOME=$HADOOP_HOME  
export HADOOP_YARN_HOME=$HADOOP_HOME  
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native  
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin  
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"  

* 하둡 환경 변수 설정

hadoop/etc/hadoop/hadoop-env.sh파일에 JAVA_HOME=/usr/local/java
 
core-site.xml, hdfs-site.xml, yarn-env.sh, yarn-site.xml, workers 수정

master 서버에 주키퍼 초기화 $HADOOP_HOME/bin/hdfs zkfc -formatZK

각 서버에 하둡 저널노드 실행 $HADOOP_HOME/bin/hdfs --daemon start journalnode

master서버 name노드 포맷 후 실행

hdfs namenode -format

$HADOOP_HOME/bin/hdfs --daemon start namenode

<h1> 2021-10-16 </h1>

* standby namenode 실행전 마스터노드의 메타데이터 복사해오기 - hdfs namenode -bootstrapStandby (standby)

여기서 계속 실패해서 애먹었는데, 포트가 127.0.0.1로 열려 있었음 (netstat -tnlp로 확인)

어찌어찌하다 다시 돌아왔는데 아마 hostname에서 localhost를 빼서일까..?

* 주키퍼 장애 컨트롤러 실행 - $HADOOP_HOME/bin/hdfs --daemon start zkfc (master, standby)

* datanode 실행 - $HADOOP_HOME/bin/hdfs --daemon start datanode

* yarn 실행 - start-yarn.sh (master에서만)

* history 서버 실행 - $HADOOP_HOME/bin/mapred --daemon start historyserver (master, standby)

<h3> 카프카 설치 </h3>

* 카프카 설치 (https://team-platform.tistory.com/13?category=829378)

wget http://apache.mirror.cdnetworks.com/kafka/2.7.1/kafka_2.12-2.7.1.tgz

tar -xvf kafka_2.12-2.7.1.tgz

* zookeeper.properties 수정

dataDir="zookeeper dataDir"

initLimit=5  
syncLimit=2  
server.1=master:2888:3888  
server.2=worker1:2888:3888  
server.3=worker2:2888:3888  

* server.properties 수정

broker.id=1  
listeners=PLAINTEXT://:9092  
advertised.listeners=PLAINTEXT://master:9092  
zookeeper.connect=master:2181, worker1:2181, worker2:2181

* kafka 서버 시작

bin/kafka-server-start.sh -daemon config/server.properties

* topic 관련

토픽 생성 : bin/kafka-topics.sh --create --zookeeper master:2181, worker1:2181, worker2:2181 --replication-factor 3 --partitions 1 --topic test_topic

토픽 삭제 : bin/kafka-topics.sh --delete --zookeeper master:2181, worker1:2181, worker2:2181 --topic test_topic

<h1> 2021-10-18 </h1>

* producer, consumer 구현을 위한 파이썬 3 설치 및 카프카 파이썬 설치

yum install epel-release  
yum install python3  
pip3 install kafka-python  

* cli에서 producer 및 consumer 테스트

consumer : bin/kafka-console-consumer.sh --bootstrap-server master:9092,worker1:9092,worker2:9092 --topic test_topic --partition 0 --from-beginning

producer : bin/kafka-console-producer.sh --broker-list master:9092,worker1:9092,worker2:9092 -topic test_topic

<h1>2021-10-20</h1>

* confluent-kafka 설치

hdfs에 적재하기 위해 이것저것 시도해보다 도저히 안됐는데

confluent-kafka에서 hdfs connector를 지원해서 그걸 사용해서 다시 해야할듯

사용법은 기존 kafka와 차이가 없는듯 하다

<h1>2021-10-25</h1>

* 스파크 설치

* test_producer로 담긴것 확인

* hdfs connector 설치 (https://www.confluent.io/hub/confluentinc/kafka-connect-hdfs)

* sink connector 생성

curl -X POST worker1:8083/connectors -H "Content-Type: application/json" -d '{  
  "name":"test",  
  "config":{  
    "connector.class": "io.confluent.connect.hdfs.HdfsSinkConnector",  
    "topics": "test",  
    "hdfs.url": "hdfs://worker1:9000",  
    "flush.size":"3"  
    }  
}'

hdfs에 저장은 안되었지만 일단 드디어 connector 생성 성공

- active node 가 worker로 되어있는데 바꿀수있는 방법이 없을까..?

<h1>2021-10-26</h1>

https://gymbombom.github.io/2019/12/11/1-hadoop-HA-cluster-install/

하둡 클러스터 세팅 깔끔한곳

하둡 초기화 통해 master node를 active로 변경, master node도 worker node로


<h1>2021-11-27</h1>

confluent kafka를 통해 hdfs로 저장하는 것은 잘 안돼서 포기..

fluentd를 통해 수집하기로 변경

설치 : curl -L https://toolbelt.treasuredata.com/sh/install-redhat-td-agent3.sh | sh

실행 : /etc/init.d/td-agent start

hdfs 연동(input : twitter): /etc/td-agent/td-agent.conf

<match twitter>  
  @type webhdfs  
  host master
  port 50070  
  path "/twitter/%Y%m%d_%H.#{Socket.gethostname}.log"  
  username gwangil  
</match>  

위내용 추가

hdfs-site.xml에 아래 내용 추가

<property>  
  <name>dfs.webhdfs.enabled</name>  
  <value>true</value>  
</property>  
<property>  
  <name>dfs.support.append</name>  
  <value>true</value>  
</property>  
<property>  
  <name>dfs.support.broken.append</name>  
  <value>true</value>  
</property>  

트위터 플러그인 설치 : stall fluent-plugin-twitter

트위터 연동

<source>  
  @type twitter  
  consumer_key 4eTTOR4C7AkZiEkhkibV5akJl  
  consumer_secret EGF0y3cxtA6xVTcO5xDZkSVtNJMACIcvPY7gpbNkmyxruGv1SC  
  access_token 1461989023363133442-kCy0KBm5JxNrZfhbDl1ytCjdVd7otz  
  access_token_secret u88CsHk52bEBdsmZSFL6H6C6iTW8eReXHATsJga5ZeZc2  
  tag twitter  
  keyword 'game'  
  output_format nest  
  timeline sampling  
  lang en  
</source>
