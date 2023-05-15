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
    return DeviceEui.objects.values_list('device_eui', flat=True)


def save_live_data(data):
    print(data)
    if(len(data) > 2):
        bus_stops = BusStops.objects.filter().values()
        device_position = np.array([data[0][0], data[0][1]])
        bus_stops_ = {}
        for each in bus_stops:
            bus_stops_[each.id] = (np.linalg.norm(device_position - [each.latitude,each.longitude]))
            bus_stop_id=min(bus_stops_, key=lambda k: bus_stops_[k])
        try:
            device_ = DeviceEui.objects.get(device_eui=data[2])
            LiveData.objects.create(
                device = device_,
                bus_stop = bus_stop_id,
                latitude = data[0][0],
                longitude = data[0][1],
                iaq = data[1]['IAQ'],
                co2 = data[1]['Co2'],
                bvoc = data[1]['BVOC'],
                temperature = data[1]['Temperature'],
                pressure = data[1]['Pressure'],
                humidity = data[1]['Humidity'],
            )
        except Exception as e:
            print(e)
    