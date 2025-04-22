# EdgeBeacon: An Edge-Assisted, LLM Agent-Powered Smart Home Automation System

## Preparation
To get EdgeBeacon setup on your system, you will need to have the following:
- A Raspberry Pi system (in our integration, we used a Pi 4 Model B 4GB, however any Pi 4/5 will suffice)
        - NOTE: Your Pi should be running Raspberry Pi OS AND needs to be connected to a router **by Ethernet** in order to utilize the Home Assistant capabilities.
- Zigbee sensors to integrate with Home Assistant (we utilized the Aqara Temperature/Humidity Sensor)
- A USB radio receiver for the Zigbee sensors
- Patience and technical know-how of running many terminal commands :)

## Installation
There are multiple steps to ensure your Pi is able to run the EdgeBeacon configuration we have provided within this repository. These steps include:
- [Updating your Raspberry Pi to Python 3.13](https://hub.tcno.co/pi/software/python-update/)
- [Installing Docker (and Docker Compose) onto the RPi]https://docs.docker.com/engine/install/raspberry-pi-os/()
- Cloning and configuring the Docker setup
- Running the EdgeBeacon configuration on your device

### Cloning and Configuring the Docker Setup
In your Raspberry Pi, open a terminal and clone the Git repository onto your system.
```
git clone https://github.com/Wag-Jack/EdgeBeacon.git
```
From here, we will need to adjust the IP address the MQTT broker is hosted on to match the IP address of your **host machine** (i.e., the Pi's default IP address). Additionally, we will need to set up a [Google Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key) for your system to work properly. First, we will configure the scheduler ML model for MQTT communication:
```
sudo nano EdgeBeacon/SchedulerML/ml.py
```
You will notice a variable named `network` in the file as seen below:<br/>
```
network = 'INSERT IP HERE'
```
Set the value of `network` to the IP address of your host machine (use `hostname -I` to figure this out), then save and exit. Next, navigate to the script hosting our reasoning LLM agent:
```
sudo nano EdgeBeacon/ReasoningAgent/agents.py
```
As before, change the value of `network` to the IP address of your host machine. Additionally, there is a command to configure a Gemini object:
```
genai.configure(api_key="INSERT KEY HERE")
```
This is where you will enter your Gemini API key once you receieve it. After changing the value of both `network` and `api_key`, save and exit. You now have your configuration ready to go!

### Running the EdgeBeacon Configuration on Your Device
Navigate to the EdgeBeacon directory:
```
cd EdgeBeacon
```
Once in here, you can start up the Docker containers by running the following command:
```
docker compose up -d
```
***NOTE: If you would like to rebuild the containers everytime (i.e. modifying files/scripts, use***
```
docker compose up --build
```
***Additionally, for testing in order to calibrate the schedule, open up a seperate terminal and find the ID of the `edgebeacon-scheduler_llm` container user***
```
docker ps
```
***Once you have found it, execute the following command***
```
docker exec -it <container_id for edgebeacon-scheduler> /bin/sh
```
***Then, within the container, execute the following:***
```
mosquitto_pub -h <ip_address of host> -p 1883 -t "zigbee2mqtt/device_id/temperature" -f zigbee0_zgb_packets_db.csv
```
This will send an example file containing the data we need to recalibrate the schedule.

**Now you are all set to use EdgeBeacon on your Raspberry Pi!**
