import paho.mqtt.client as paho
from time import sleep
from pycomm3 import LogixDriver
from queue import Queue
q=Queue()
broker="160.75.154.101" #mqtt cloud ip'si
port=1884
username="iturockwell"
password="963258741"
msg0 = "bora"

def on_message(client, userdata, message): #MQTT topic'e subscribe olma
    #time.sleep(1)
    #global IntVal
    value = str(message.payload.decode("utf-8"))
    print(value)
    IntVal = int(value)
    global data #bağlanılan topicten gelen veri
    global dataTopic #bağlanılan topic ismi

    data = str(message.payload.decode("utf-8"))
    dataTopic = str(message.topic)


client= paho.Client("client-001")
######Bind function to callback
client.on_message=on_message
#####
client.username_pw_set(username, password)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
client.subscribe("BoraDeneme",0)#subscribe



while True:
    print(data)
    print(dataTopic)
    client.publish("BoraDeneme1",msg0) #plc verilerini mqtt cloud'a paylaşma
    

#Node-Red