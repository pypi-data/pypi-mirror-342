import unittest
import sys, os
from atk_common.http_utils import get_test_response

class TestHttpUtils(unittest.TestCase):

    def test_get_test_response_none(self):
        resp_json = get_test_response()
        self.assertIsNotNone(resp_json)

    def test_get_image_version_not_none_1(self):
        resp_json = get_test_response('bo-config-db-api')
        self.assertIsNotNone(resp_json)

    def test_get_image_version_not_none_2(self):
        resp_json = get_test_response('bo-case-web')
        self.assertIsNotNone(resp_json)

if __name__ == "__main__":
    unittest.main()
