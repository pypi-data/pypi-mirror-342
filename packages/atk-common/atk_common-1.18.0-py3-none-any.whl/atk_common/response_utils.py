from atk_common.enums.response_status_enum import ResponseStatus

def create_response(status, status_code, response_msg):
    data = {}
    data['status'] = status
    data['statusCode'] = status_code
    data['responseMsg'] = response_msg
    return data

def is_response_ok(response):
    return response['status'] == ResponseStatus.OK
