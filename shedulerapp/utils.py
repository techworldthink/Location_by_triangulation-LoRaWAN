from adminapp.models import Chirpstack
from adminapp.models import DeviceEui

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