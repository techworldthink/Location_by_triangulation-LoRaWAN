import numpy as np

from adminapp.models import Chirpstack
from adminapp.models import DeviceEui
from adminapp.models import LiveData
from adminapp.models import BusStops

def get_chirp_credentials():
    credentials = []
    try:
        chirp_obj = Chirpstack.objects.first()
        credentials.append(chirp_obj.server_url)
        credentials.append(chirp_obj.user_name)
        credentials.append(chirp_obj.password)
    except:
        pass
    return credentials


def get_devices():
    return list(DeviceEui.objects.values_list('device_eui', flat=True))


def save_live_data(data):
    print("--SAVE - TRY")
    if(len(data) > 2):
        bus_stops = BusStops.objects.filter().values()
        device_position = np.array([data[0][0], data[0][1]])
        bus_stops_ = {}
        for each in bus_stops:
            bus_stops_[each['id']] = (np.linalg.norm(device_position - [float(each['latitude']),float(each['longitude'])]))
            bus_stop_id=min(bus_stops_, key=lambda k: bus_stops_[k])
        try:

            device_ = DeviceEui.objects.get(device_eui=data[2])
            bus_instance = BusStops.objects.get(id=bus_stop_id)
            device_eui = device_.device_eui
            
            try:
                live_data = LiveData.objects.filter(device_eui=device_eui,frame_count=data[1]).last()
                if live_data is None:
                    print("IGNORE - UPDATE LIVE DATA")
                    return
                live_data.device = device_
                live_data.bus_stop = bus_instance
                live_data.latitude = data[0][0]
                live_data.longitude = data[0][1]
                live_data.save(update_fields=["device","bus_stop","latitude","longitude"])
                print("--OK")
            except Exception as e:
                print("ERROR - UPDATE LIVE DATA")
                print(e)
            
            
        except Exception as e:
            print("--ERROR")
            print(e)
    

def save_data_only(data):
    LiveData.objects.create(
        iaq = data['IAQ'],
        co2 = data['Co2'],
        bvoc = data['BVOC'],
        temperature = data['Temperature'],
        pressure = data['Pressure'],
        humidity = data['Humidity'],
        device_eui = data['devEUI'],
        frame_count = data['fCnt']
    )