# Smart-Greenhouse

This is a demo project to show how a traditional greenhouse can be transformed using IOT, Isilon Big Data Analytics and AI.
Here is a [demo video](https://youtu.be/SFN2EIOu6mc).
![Smart Greenhouse Architecture Diagram](/Smart-Greenhouse.png)

## Setup:
Clone this repo to a Linux machine (Centos 7.4). This will be the Image Recognition VM.

	git clone https://github.com/siaut/Smart-Greenhouse.git 
### Raspberry Pi:
1.Setup Raspberry Pi with Raspbian. 

2.Copy RaspberryPi/gh-sensors directory to /root/iot/gh-sensors.

3.Configure and run these 2 services: 

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



