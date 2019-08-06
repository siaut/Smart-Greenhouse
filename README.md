# Smart-Greenhouse

This is a demo project to show how a traditional greenhouse can be transformed using IOT, Isilon Big Data Analytics and AI.
Here is a [demo video](https://youtu.be/SFN2EIOu6mc).
![Smart Greenhouse Architecture Diagram](/Smart-Greenhouse.png)

## Setup:
Clone this repo to a Linux machine (Centos 7.4). This will be the Image Recognition VM.

	git clone https://github.com/siaut/Smart-Greenhouse.git 
### Raspberry Pi:
1. Setup Raspberry Pi with Raspbian. 

2. Copy RaspberryPi/gh-sensors directory to /root/iot/gh-sensors.

3. Configure and run these 2 services: 

		startsensors.sh
		controller.sh
    
### Dell Edge Gateway 5000:
1. Install Ubuntu desktop 16.04 in Edge Gateway

2. Install MQTT([Mosquitto Broker](https://www.vultr.com/docs/how-to-install-mosquitto-mqtt-broker-server-on-ubuntu-16-04)):

3. Copy DellEdgeGateway to /opt/greenhouse

4. Configure and run these 3 services:

		gwcontroller.service
		readsensors.service
		web-gwcontroller.service

### Image Recognition VM:
1. Get a google map API key from:
https://developers.google.com/maps/documentation/javascript/get-api-key

2. Install [PCF CLI client](https://docs.pivotal.io/pivotalcf/2-3/cf-cli/install-go-cli.html)

3. Login to PAS (Cloud Foundry), subscribe MySQL and Redis.
	
		cf login -a api.system.abc.com --skip-ssl-validation
		cf create-service p.mysql db-small iot
 		cf create-service p.redis cache-small redis1
    
   Push gh-controller:
   
   		cd CloudFoundry/gh-controller
   		cf push gh-controller
   
   Push greenhouse:
   
   		cd CloudFoundry/greenhouse
   		cf push greenhouse
    
   Bind the services:    
   
		cf bind-service gh-controller iot
		cf bind-service gh-controller redis1
   		cf bind-service greenhouse iot
		cf bind-service greenhouse  redis1

   Create environment variables:
   
 		#cf set-env greenhouse weatherkey xxx
		cf set-env greenhouse mapkey YYY
    
   Restage the applications:
   
		cf restage gh-controller
		cf restage greenhouse
		
4. Deploy [PivotalMySQLWeb](https://github.com/pivotal-cf/PivotalMySQLWeb)
5. Login to PivotalMySQLWeb to create these tables:
	

		DROP TABLE IF EXISTS sensors;
		create table sensors(
		ctime DATETIME,
		   temp float ,
		   light int,
		   moisture float,      
		   distance float,
		   led int,
		   fan int,
		   waterpump int,   
		   PRIMARY KEY ( ctime )
		);

		DROP TABLE IF EXISTS alerts;
		create table alerts(
		ctime DATETIME,
		   filename varchar(255) ,
		   distance float,
		   aws text,
		   msvision text,   
		   PRIMARY KEY ( ctime )
		);

6. Install [Tensorflow](https://www.tensorflow.org/install):

		yum -y install epel-release
		yum -y update
		yum -y install gcc gcc-c++ gcc-gfortran openssl-devel libffi-devel python-pip python-devel atlas atlas-devel
		pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.7.0-cp27-none-linux_x86_64.whl
				
7. Install screen:

		yum -y install screen
		
8. Start screen and run the tensorflow image recognition application:

		screen
		image-recognition-vm/start-image-recognition.sh
		
9. Setup [Isilon and HortonWorks](https://www.emc.com/collateral/TechnicalDocument/docu71396.pdf).
Install Spark2, Hive, NiFi and Zeppelin.

10. Create user in Isilon:

		isi auth groups create nifi --zone hdpzone --provider local
		isi auth users create nifi --primary-group nifi \
		--zone hdpzone --provider local \
		--home-directory /ifs/hdp/hadoop/user/nifi

11. Add user to Hadoop nodes. This is performed on the master node:

		useradd -u 2003 nifi
		sudo -u hdfs hdfs dfs -mkdir -p /user/nifi
		sudo -u hdfs hdfs dfs -chown nifi:nifi /user/nifi
		sudo -u hdfs hdfs dfs -chmod 755 /user/nifi

12. Create a database in Hive to store historical data:

		SSH to the master node
		beeline
		!connect jdbc:hive2://masterdns.pgen6.local:2181,pnode2.pgen6.local:2181,pnode1.pgen6.local:2181/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2
		create database smartgreenhouse;

		use smartgreenhouse;

		CREATE TABLE greenhouse2
		(
		   currenttime TIMESTAMP,
		   light INT,
		   moisture DOUBLE,
		   temperature DOUBLE,
		   distance DOUBLE
		)
		CLUSTERED BY (currenttime)INTO 24 BUCKETS
		ROW FORMAT DELIMITED
		STORED AS ORC 
		TBLPROPERTIES('transactional'='true');
		
13. Create a NiFi Flow.	Open NiFi and import NiFi/Greenhouse_v2.xml template.
14. Create a Zeppelin notebook. Open Zeppelin and import Zeppelin/Smart Greenhouse.json note.
