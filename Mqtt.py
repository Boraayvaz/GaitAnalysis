import paho.mqtt.client as paho
from time import sleep
from pycomm3 import LogixDriver
from queue import Queue
q=Queue()
broker="160.75.154.74" #mqtt cloud ip'si
port=1883

data = '0'
dataTopic = ''


global IntVal




plc2 = LogixDriver('172.16.2.5', init_tags=False) #plc ethernet bağlantısı. Uygun IPyi gir
plc3 = LogixDriver('172.16.3.44', init_tags=False)
print(plc2)
print(plc3)
plc2.get_tag_list() #PLC'den tagleri alma
plc3.get_tag_list()

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

client.connect(broker)#connect
client.loop_start() #start loop to process received messages
client.subscribe("LAMP1",0)#subscribe
client.subscribe("LAMP2",0)#subscribe
client.subscribe("LAMP3",0)#subscribe
client.subscribe("LAMP4",0)#subscribe
client.subscribe("LAMP5",0)#subscribe
client.subscribe("LAMP6",0)#subscribe
client.subscribe("LAMP7",0)#subscribe
client.subscribe("LAMP8",0)#subscribe
client.subscribe("LAMP9",0)#subscribe
client.subscribe("LAMP10",0)#subscribe
client.subscribe("LAMP11",0)#subscribe
client.subscribe("LAMP12",0)#subscribe
client.subscribe("RotaryActivate",0)#subscribe
client.subscribe("RotaryStart",0)#subscribe


while True:
    msg0 = plc2.read('LAMP_1')[1] #plc'den tag okuma
    msg1 = plc2.read('LAMP_2')[1] #plc'den tag okuma
    msg2 = plc2.read('LAMP_3')[1]#plc'den tag okuma
    msg3 = plc2.read('LAMP_4')[1] #plc'den tag okuma
    msg4 = plc2.read('LAMP_5')[1] #plc'den tag okuma
    msg5 = plc2.read('LAMP_6')[1]#plc'den tag okuma
    msg6 = plc2.read('LAMP_7')[1] #plc'den tag okuma
    msg7 = plc2.read('LAMP_8')[1] #plc'den tag okuma
    msg8 = plc2.read('LAMP_9')[1]#plc'den tag okuma
    msg9 = plc2.read('LAMP_10')[1] #plc'den tag okuma
    msg10 = plc2.read('LAMP_11')[1] #plc'den tag okuma
    msg11 = plc2.read('LAMP_12')[1]#plc'den tag okuma
    Rcounter = plc3.read('counter.ACC')[1]#plc'den tag okuma
    RBeltSpeed = plc3.read('belt_speed')[1]#plc'den tag okuma
    RKnifeSpeed = plc3.read('knife_speed')[1]#plc'den tag okuma
    RExpected= plc3.read('exp_result')[1]#plc'den tag okuma
    RActualPosition= plc3.read('knife.ActualPosition')[1]#plc'den tag okuma
    RCommdVel= plc3.read('knife.CommandVelocity')[1]#plc'den tag okuma
    RBeltAverageVelocity= plc3.read('belt.AverageVelocity')[1]#plc'den tag okuma



    dataInt = int(data)
    print(dataTopic)
    client.publish("LAMP_0",msg0) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_1",msg1) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_2",msg2) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_3",msg3) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_4",msg4) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_5",msg5) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_6",msg6) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_7",msg7) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_8",msg8) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_9",msg9) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_10",msg10) #plc verilerini mqtt cloud'a paylaşma
    client.publish("LAMP_11",msg11) #plc verilerini mqtt cloud'a paylaşma
    client.publish("counterCV",Rcounter) #plc verilerini mqtt cloud'a paylaşma
    client.publish("belt_speed",RBeltSpeed) #plc verilerini mqtt cloud'a paylaşma
    client.publish("knife_speed",RKnifeSpeed)  #plc verilerini mqtt cloud'a paylaşma
    client.publish("knife_act_pos",RActualPosition)  #plc verilerini mqtt cloud'a paylaşma
    client.publish("belt_avg_vel",RBeltAverageVelocity)  #plc verilerini mqtt cloud'a paylaşma
    client.publish("knife_comd_vel",RCommdVel)  #plc verilerini mqtt cloud'a paylaşma
    client.publish("expected",RExpected)  #plc verilerini mqtt cloud'a paylaşma

    if dataInt == 1:
        boolean = False
    elif dataInt ==0:
        boolean = True

    if dataTopic == "LAMP1":
        plc2.write(('LAMP_1', boolean))

    if dataTopic == "LAMP2":
        plc2.write(('LAMP_2', boolean))

    if dataTopic == "LAMP3":
        plc2.write(('LAMP_3', boolean))

    if dataTopic == "LAMP4":
        plc2.write(('LAMP_4', boolean))

    if dataTopic == "LAMP5":
        plc2.write(('LAMP_5', boolean))

    if dataTopic == "LAMP6":
        plc2.write(('LAMP_6', boolean))

    if dataTopic == "LAMP7":
        plc2.write(('LAMP_7', boolean))

    if dataTopic == "LAMP8":
        plc2.write(('LAMP_8', boolean))

    if dataTopic == "LAMP9":
        plc2.write(('LAMP_9', boolean))

    if dataTopic == "LAMP10":
        plc2.write(('LAMP_10', boolean))

    if dataTopic == "LAMP11":
        plc2.write(('LAMP_11', boolean))

    if dataTopic == "LAMP12":
        plc2.write(('LAMP_12', boolean))

    if dataTopic == "RotaryActivate":
        plc3.write(('activateCont', not(boolean)))

    if dataTopic == "RotaryStart":
        plc3.write(('startCont', boolean))

    sleep(0.1)
#Node-Red
