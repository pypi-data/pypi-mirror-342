import docker
import socket
from atk_common.log_utils import add_log_item

def get_image_name_and_version(tags):
    if tags:
        # Use the first tag (usually only one)
        full_tag = tags[0]  # e.g., 'bo-crypto-wrapper-api:latest'

        if ":" in full_tag:
            image_name, image_version = full_tag.split(":", 1)
        else:
            image_name = full_tag
            image_version = "<none>"
        return image_name, image_version
    else:
        return None, None
    
def create_port_item(port, binding):
    data = {}
    data['port'] = port
    data['binding'] = binding
    return data

def create_container_log(container_data):
    log_str = 'Container name: ' + container_data['containerName'] + ', image name: ' + container_data['imageName'] + ', image version: ' + container_data['imageVersion']
    add_log_item(log_str)

def get_current_container_info():
    try:
        data = {}
        client = docker.from_env()

        # Get current container's hostname (usually the container ID)
        container_id = socket.gethostname()

        # Fetch container object using partial ID
        container = client.containers.get(container_id)

        tags_info = get_image_name_and_version(container.image.tags)
        data['imageName'] = tags_info[0]
        data['imageVersion'] = tags_info[1]
        data['containerName'] = container.name
        ports = container.attrs['NetworkSettings']['Ports']
        data['ports'] = []
        if ports:
            for container_port, host_bindings in ports.items():
                if host_bindings:
                    for binding in host_bindings:
                        data['ports'].append(create_port_item(container_port, f"{binding['HostIp']}:{binding['HostPort']}"))
                else:
                    data['ports'].append(create_port_item(container_port, None))
        create_container_log(data)
        return data
    except Exception as e:
        add_log_item("Error getting container data:" + str(e))
        return None
