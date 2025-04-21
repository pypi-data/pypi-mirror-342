import docker
import os
import socket
from atk_common.env_utils import get_env_value

def find_image_prop_list_by_name(image_list, image_name):
    for image in image_list:
        if image.tags and len(image.tags) > 0:
            # Check if the image name is in the first tag
            if image_name in image.tags[0]:
                return image.tags[0]
    return None

def get_image_version(default_value=None):
    """
    Get the version of a Docker image.
    
    :param image_name: Name of the Docker image
    :return: Version of the Docker image
    """
    try:
        image_name = get_env_value('DOCKER_IMAGE_NAME', default_value)
        if image_name is None:
            return None
        client = docker.from_env()
        image_list = client.images.list()
        image_prop_list = find_image_prop_list_by_name(image_list, image_name)
        if image_prop_list is None:
            return None
        image_props = image_prop_list.split(':')
        if len(image_props) < 2:
            return None
        return image_props[1] 
    except docker.errors.ImageNotFound:
        return None

def get_current_container_info():
    try:
        client = docker.from_env()

        # Get current container's hostname (usually the container ID)
        container_id = socket.gethostname()

        # Fetch container object using partial ID
        container = client.containers.get(container_id)

        name = container.name
        ports = container.attrs['NetworkSettings']['Ports']

        print(f"🔍 Container name: {name}")
        print("🌐 Port mappings:")
        if ports:
            for container_port, host_bindings in ports.items():
                if host_bindings:
                    for binding in host_bindings:
                        print(f"  {container_port} -> {binding['HostIp']}:{binding['HostPort']}")
                else:
                    print(f"  {container_port} -> Not bound to host")
        else:
            print("No exposed ports found.")
        return None

    except Exception as e:
        print("❌ Error getting container info:", e)
        return None
