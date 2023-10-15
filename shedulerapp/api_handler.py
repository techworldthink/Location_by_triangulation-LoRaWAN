import requests
from datetime import date
import json
import base64
import threading
from .triangulation import triangulate
import traceback
from .utils import save_live_data
from .mqtt_handler import run_mqtt

today = date.today()

run_thread = []

# LORASERVER -  credentials & urls
EMAIL_LIST = []
PASSWORD_LIST = []
LORASERVER_URL_LIST=[]
DEV_EUIS = []

                                                                                                                                                                                                                                                                                                                                                                                                              

# get jwt token
def apilogin(email,password,url):
  url=url+'/api/internal/login'
  credentials = '{"password": "'+password+'","email": "'+email+'"}'
  headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
  x = requests.post(url, data = credentials, headers=headers)
  data = x.json()
  return data['jwt']

    
# check frame type 
def get_frame_type(json_data):
    if "result" in json_data:
        json_data = json_data['result'] 
        if "uplinkFrame" in json_data:
            json_data = json_data['uplinkFrame'] 
        if "downlinkFrame" in json_data:
            json_data = json_data['downlinkFrame']    
        if "phyPayloadJSON" in json_data:
            json_data = json_data['phyPayloadJSON']  
        if "mhdr" in json_data:
            temp = json.loads(json_data)
            if "mType" in temp["mhdr"]:
                return temp["mhdr"]["mType"]
    return ""


# return Unconfirmed Data
def handle_unconf_up_data(json_data,device_eui):
    data = get_up_data(json_data,device_eui)
    save_live_data(data)
    
# return Confirmed Data
def handle_conf_up_data(json_data,device_eui):
    data = get_up_data(json_data,device_eui)
    save_live_data(data)


# get the count of same packet receivers gateway 
def get_received_gtw_count(rxInfo):
    return len(rxInfo)


# check the frame contain -  Unconfirmed up / Confirmed up / Join request data 
# if found return data else null
def get_up_data(json_data,device_eui):
    if "result" in json_data:
        json_data = json_data['result'] 
        if "uplinkFrame" in json_data:
            json_data = json_data['uplinkFrame'] 
            if "phyPayloadJSON" in json_data:
                rxInfo = json_data['rxInfo']
                gtw_count = get_received_gtw_count(rxInfo)
                triangulation_data = []
                print(device_eui)
                print("---------------------------------------------------")
                for gtw in rxInfo:
                    gtw_data = []
                    if(gtw['fineTimestampType'] == 'NONE'):
                        # ignore
                        print(base64.b64decode(gtw['gatewayID']).hex()," - ","NONE")
                        continue
                    else:
                        print(base64.b64decode(gtw['gatewayID']).hex()," - ",gtw['plainFineTimestamp']['time'])
                    gtw_data.append(gtw['time'])
                    gtw_data.append(base64.b64decode(gtw['gatewayID']).hex())
                    gtw_data.append(gtw['plainFineTimestamp']['time'])
                    gtw_data.append(gtw['location']['latitude'])
                    gtw_data.append(gtw['location']['longitude'])
                    gtw_data.append(gtw['rssi'])
                    triangulation_data.append(gtw_data)
                print("---------------------------------------------------")

                # data  fetch
                json_data = json_data['phyPayloadJSON'] 
                temp = json.loads(json_data)
                frame_count = temp['macPayload']['fhdr']['fCnt']
                print(frame_count)

                #bytes_data = temp['macPayload']['frmPayload'][0]['bytes']
                #bytes_data_ = bytes(ord(c) for c in bytes_data)

                # triangulate
                if(len(triangulation_data) > 1):
                    timestamps = []
                    locations = []
                    for t_data in triangulation_data:
                        timestamps.append(t_data[2])
                        locations.append([t_data[3],t_data[4]])
                    data = triangulate(timestamps,locations)
                    return [data,frame_count,device_eui]
                else:
                    print("-NGTW CNT < 2-")

                return []

            

def monitor_thread(device_eui,url,headers,CREDENTIALS):
    print("-- STATUS - START - thread - Device " + device_eui)
    response = requests.get(url+"/api/devices/"+device_eui+"/frames", headers=headers, stream=True)

    # If token expires, regenerate
    if(response.status_code == 401):
        LORASERVER_TOKEN=apilogin(CREDENTIALS[0],CREDENTIALS[1],CREDENTIALS[2])
        headers = { "Accept": "application/json","Grpc-Metadata-Authorization": "Bearer "+LORASERVER_TOKEN}
        monitor_thread(device_eui,url,headers,CREDENTIALS)

    for data in response.iter_content(chunk_size=None):
        string_data = data.decode('utf-8')
        try:
            json_data = json.loads(string_data)
            frame_type = get_frame_type(json_data)

            if(frame_type == "UnconfirmedDataUp"):
                handle_unconf_up_data(json_data,device_eui)
            elif(frame_type == "ConfirmedDataUp"):
                handle_conf_up_data(json_data,device_eui)
        except Exception as e:
            print("---JSONDecodeError")
            traceback.print_exc()
    print("-- STATUS - END - thread - Device " + device_eui)

# get frames and check for join requests
def monitor_and_save_frames(url,LORASERVER_TOKEN,CREDENTIALS):
    # print("--START check and save frames")
    headers = { "Accept": "application/json","Grpc-Metadata-Authorization": "Bearer "+LORASERVER_TOKEN}
    # thread code add here....
    for device_eui in DEV_EUIS:
        print(" --Thread  -Device : " + device_eui)
        run_thread.append(threading.Thread(target=monitor_thread, args=(device_eui,url,headers,CREDENTIALS,)))
    # MQTT    
    run_thread.append(threading.Thread(target=run_mqtt, args=(DEV_EUIS)))
    # print("--END check and save frames")


    
def threads_close():
    while(1):
        for each in run_thread:
            each.join()
        print("close all threads")



def main():
    global DEV_EUIS               
    while(1):
        for x in range(len(LORASERVER_URL_LIST)):
            print("--START URL : " + LORASERVER_URL_LIST[x])
            LORASERVER_URL = LORASERVER_URL_LIST[x]
            email=EMAIL_LIST[x]
            password=PASSWORD_LIST[x]
            LORASERVER_TOKEN=apilogin(email,password,LORASERVER_URL)
            print("DEV_EUIS : ->")
            print(DEV_EUIS)
            print("--START - monitoring")
            monitor_and_save_frames(LORASERVER_URL,LORASERVER_TOKEN,[email,password,LORASERVER_URL])
            # print("--END URL : " + LORASERVER_URL_LIST[x])  
            # print("\n\n\n")
            print("Running ...... ")
            print("\n\n\n")

      
        for each in run_thread:
            each.start()

        # token_regenerate_thread = threading.Thread(target=threads_close, args=())
        # token_regenerate_thread.start()

        for each in run_thread:
            each.join()
        
        print("\n\n------------------------ Restart (API - regenerate) ----------------------------------\n\n")
        
        

def analysis_frames(credentials,devices):
    global DEV_EUIS
    global EMAIL_LIST 
    global PASSWORD_LIST 
    global LORASERVER_URL_LIST

    if(len(credentials) < 3):
        print('-Invalid credentials-')
        return
    
    LORASERVER_URL_LIST = [credentials[0]]
    EMAIL_LIST = [credentials[1]]
    PASSWORD_LIST = [credentials[2]]
    DEV_EUIS = devices
    
    main()