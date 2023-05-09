from background_task import background
from datetime import timedelta
from background_task.models import Task
import time


@background(schedule=1)
def live_frame_analysis():
    print('start')
    while True:
        try:
            print('.')
            time.sleep(10)
        except:
            print('-Restart-')
            live_frame_analysis.schedule(retry=True, delay=1)

def activate_live_frame_analysis():
    try:
        Task.objects.get(task_name='live_frame_analysis')
    except:
        live_frame_analysis(repeat=None)

