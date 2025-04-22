import paho.mqtt.client as mqtt
import sqlite3 as sql
import time

#Broker attributes
sub_topic = 'scheduler/final'

#Change to your host network
network = 'INSERT IP HERE'
port = 1883
keepalive = 0

#Function to initialize events.db if it does not exist within the directory
def insert_table(file):
    cnt = sql.connect('events.db')

    #Create DATE table
    DATE = '''CREATE TABLE IF NOT EXISTS Date (
                Date_ID SERIAL PRIMARY KEY,
                Month INT NOT NULL,
                Day INT NOT NULL,
                Year INT NOT NULL,
                Hour INT NOT NULL,
                Minute INT NOT NULL,
                Second INT NOT NULL,
                UNIQUE (Month, Day, Year, Hour, Minute, Second)
            );'''

    #Create EVENTS table
    EVENTS = '''CREATE TABLE IF NOT EXISTS Events (
                Event_ID SERIAL PRIMARY KEY,
                Event_Name VARCHAR(255) NOT NULL,
                Time_ID INT NOT NULL,
                Sensor_Used VARCHAR(255)
            );'''

    #Create AGENT_COMMANDS table
    AGENT_COMMANDS = '''CREATE TABLE IF NOT EXISTS Agent_Commands (
                        Command_ID SERIAL PRIMARY KEY,
                        Event_ID INT,
                        Command VARCHAR(255) NOT NULL,
                        FOREIGN KEY (Event_ID) REFERENCES Events(Event_ID)
            );'''
    
    #Create SCHEDULE table
    SCHEDULE = '''CREATE TABLE IF NOT EXISTS Schedule (
                    Schedule_ID SERIAL PRIMARY KEY,
                    Date_ID INT,
                    Event_ID INT,
                    Schedule_Order INT,
                    FOREIGN KEY (Date_ID) REFERENCES Dates(Date_ID),
                    FOREIGN KEY (Event_ID) REFERENCES Events(Event_ID)
            );'''

    #Generate each table within the database
    cnt.execute(DATE)
    cnt.execute(EVENTS)
    cnt.execute(AGENT_COMMANDS)
    cnt.execute(SCHEDULE)

    with open(file, 'rb') as f:
        for line in f:
            cnt.execute(f'''INSERT INTO EVENTS VALUES {line.strip()}''')

    print(f'event.db successfully updated from contents of {file}!')

#Function to process an incoming schedule from the subscribed topic
def process_schedule(message):
    payload = message.payload.decode('ascii')
    insert_table(payload)

#Callback messages for broker
def on_connect(client, data, flags, rc, properties=None):
    if rc == 0:
        print(f'Home Assistant container connected with result code {rc}')
        client.subscribe(sub_topic)
    else:
        print(f'Home Assistant container failed to connect, result code {rc}')

def on_disconnect(client, data, flags, rc, properties=None):
    print(f'Home Assistant container disconnected with result code {rc}')

def on_message(client, data, message):
    print(f'Message received: {message.payload.decode} on topic {message.topic}')
    process_schedule(message)

#New MQTT client
broker = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

#Callback functions
broker.on_connect = on_connect
broker.on_disconnect = on_disconnect
broker.on_message = on_message

#Loop to ensure script does not exit early / constant reboot
while True:
    try:
        broker.connect(network, port, keepalive)
        broker.loop_start()

        #Keeps main thread alive
        while True:
            time.sleep(1)

    except Exception as e:
        print(f'Connection on Home Assistant container interrupted, retrying (Reason: {e})')

    finally:
        broker.loop_stop()
        broker.disconnect()
