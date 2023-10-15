import paho.mqtt.client as mqtt
import json
from .utils import save_data_only

device_euis = []

uplink_topic = 'application/17/#'
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to the desired MQTT topic(s)
    client.subscribe("application/17/#")

# def on_message(client, userdata, msg):
#     print("Received MQTT message: " + msg.topic + " " + str(msg.payload))

def on_message(client, userdata, msg):
    output=json.loads(msg.payload.decode()) 
    #print(output)
    data = {}
    data['devEUI'] = output['devEUI']
    try:
        if('fCnt' not in output):
            print("Join request - avoid frame")
            return
        if(data['devEUI'] in device_euis):
            data['fCnt'] = output['fCnt']
            # data['IAQ'] = output['object']['IAQ']
            # data['Co2'] = output['object']['Co2']
            # data['BVOC'] = output['object']['BVOC']
            # data['Humidity'] = output['object']['Humidity']
            # data['Pressure'] = output['object']['Pressure']
            # data['Temperature'] = output['object']['Temperature']

            data['IAQ'] = 3
            data['Co2'] = 1
            data['BVOC'] = 1
            data['Humidity'] = 1
            data['Pressure'] = 1
            data['Temperature'] = 1


            save_data_only(data)
            print("-- SAVE - MQTT Data")
    except Exception as e:
        print("ERROR - MQTT SAVE")
        print(e)



# Create an MQTT client and configure callbacks
client = mqtt.Client("lorawan_triangulation")
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.username_pw_set("admin", "WV9jLN74")  # Set authentication credentials if required
client.connect("mqtt2.openiot.in", 1883, 60)

def run_mqtt(devices):
    print("Devices : ",devices)
    print("-- STATUS - START - thread - MQTT")
    global device_euis
    device_euis = devices
    # Start the MQTT loop to maintain the connection and process messages
    client.loop_forever()
