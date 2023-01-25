import paho.mqtt.client as paho
from time import sleep
from queue import Queue
import thread
q=Queue()
broker="160.75.154.101" #mqtt cloud ip'si
port=1884
username="iturockwell"
password="963258741"
msg0 = 5
data = '0'
dataTopic = ''
topic1 = "topic1"
topic2 = "topic2"
Qos = 0
def on_message(client, userdata, message): #MQTT topic'e subscribe olma
    value = str(message.payload.decode("utf-8"))
    global data
    global dataTopic 
    data = str(message.payload.decode("utf-8"))
    dataTopic = str(message.topic)


client= paho.Client("client-001")
######Bind function to callback
client.on_message=on_message
#####
client.username_pw_set(username, password)
client.connect(broker, port)#connect
client.loop_start() #start loop to process received messages
#subscribe

def subscribe(topic, Qos)
    client.subscribe(topic,Qos)
    global SubData
    SubData = data
    return SubData

def publish(topic, msg):
    client.publish(topic,msg)
    print("Data Published")
 
try: 
    thread.start_new_thread(subscribe, (topic1, Qos))
    thread.start_new_thread(publish, (topic2, msg0))
except: 
    print "Error while threading"
   
while 1:
    pass
    
    