import datetime
import time
import json
import paho.mqtt.client as mqtt

mqttsub = "MQTT/SETTIMER/"
mqtttitle = "MQTT_TIMER"

time.sleep( 5 )
print( "start init" )

def on_connect( client, userdata, flags, rc ):
    client.subscribe( mqttsub )
    time.sleep( 5 ) 
    print( "subscribed" )
    
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode()
    
    print( "receive " + str( msg.topic ) + " = " + str( msg.payload ) )
    if( msg.topic==mqttsub ):
        #{"time":"' + dtString + '","channel":"'+channel+'"}
        #expected json: {"time":"19:59","channel":"22"}
        jsn = json.loads( msg.payload )
        current_time = datetime.datetime.now()
        now = current_time.strftime("%H:%M:%S")
        
        tmr = jsn["time"]
        print("Set Timer to " + tmr + " at " + now)
        timerlist.append( jsn )

client2 = mqtt.Client( mqtttitle )
client2.on_connect = on_connect
client2.on_message = on_message
client2.username_pw_set( "admin", "admin" )

client2.connect( "192.168.0.110", 1883, 240 )
client2.loop_start()

timerlist = []
current_time = datetime.datetime.now()
now = current_time.strftime("%H:%M:%S")

print( "now is ", now )

def main():
    while True:
        current_time = datetime.datetime.now()
        now = current_time.strftime("%H:%M:%S")
        
        for tmr in timerlist:
            date = tmr["time"]
            channel = tmr["channel"]
            if now == date:
                print("Time to Wake up " + date + " switch to " + channel )
                for char in channel:
                    print( "sending ", char )
                    client2.publish( "MQTT/TIMEREVENT", char, qos=0, retain=False )
                    time.sleep(1)
        time.sleep(1)
      
if __name__=="__main__":
    main()
