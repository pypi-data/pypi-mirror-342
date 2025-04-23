import json
from atk_common.datetime_utils import get_utc_date_time
from atk_common.docker_utils import get_current_container_info
from atk_common.env_utils import get_env_value

def is_status_code_ok(status_code):
    return status_code >= 200 and status_code < 300

def get_test_response():
    data = {}
    container_info = get_current_container_info()
    if container_info is not None:
        data['imageName'] = container_info['imageName']
        data['imageVersion'] = container_info['imageVersion']
        data['containerName'] = container_info['containerName']
        data['containerPorts'] = container_info['ports']
    else:
        data['imageName'] = None
        data['imageVersion'] = None
        data['containerName'] = None
        data['containerPorts'] = None
    data['timestamp'] = get_utc_date_time()
    return data

def get_test_response(docker_container_data, component):
    data = {}
    data['utcDateTime'] = get_utc_date_time()
    if docker_container_data is None:
        data['containerData'] = None
        data['component'] = component
    else:
        data['containerData'] = docker_container_data
    return data
