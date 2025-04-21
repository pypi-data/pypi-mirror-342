import json
from atk_common.datetime_utils import get_utc_date_time
from atk_common.docker_utils import get_current_container_info, get_image_version
from atk_common.env_utils import get_env_value

def is_status_code_ok(status_code):
    return status_code >= 200 and status_code < 300

def get_test_response(default_value=None):
    data = {}
    container_info = get_current_container_info()
    if container_info is not None:
        data['containerName'] = container_info.name
        data['containerPorts'] = container_info.ports
    else:
        data['containerName'] = None
        data['containerPorts'] = None
    data['imageName'] = get_env_value('DOCKER_IMAGE_NAME', default_value)
    if data['imageName'] is None:
        data['imageVersion'] = None
    else:
        data['imageVersion'] = get_image_version(data['imageName'])
    data['timestamp'] = get_utc_date_time()
    return json.dumps(data)