import unittest
import sys, os
from atk_common.error_utils import get_error_entity

class TestErrorUtils(unittest.TestCase):

    def create_dummy_container_info(self):
        data = {}
        data['imageName'] = 'bo-test-api'
        data['imageVersion'] = '1.0.0'
        data['containerName'] = 'bo-test-api'
        data['ports'] = []
        data['ports'].append({'port': 8080, 'binding': 8080})
        return data

    def test_get_error_entity(self):
        resp_json = get_error_entity(None, 'An new error occured', 'get-configuration', 1, 404, self.create_dummy_container_info())
        self.assertIsNone(resp_json)

if __name__ == "__main__":
    unittest.main()
