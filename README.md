Instruction setup tracelog from scratch
=======================================


## Cassandra

Install Cassandra: http://cassandra.apache.org/download/

Use cassandra.yaml -> /etc/cassandra/cassandra.yaml


## Haproxy

Install haproxy: `sudo apt-get install haproxy`

Use haproxy.cfg -> /etc/haproxy/haproxy.cfg


## Supervisor

Install supervisor: `sudo apt-get install supervisor`

Use supervisord.conf -> /etc/supervisor/supervisord.conf


## Zeppelin

Install zepplin: http://www.apache.org/dyn/closer.cgi/zeppelin/zeppelin-0.7.1/zeppelin-0.7.1-bin-all.tgz

Download and extract, then run `bin/zeppelin-daemon.sh start`

To stop the server use `bin/zeppelin-daemon.sh stop`


## Thrift & others

Install click: `sudo pip install click`

Install thrift using provided tar. `./configure` -> `sudo make install`

