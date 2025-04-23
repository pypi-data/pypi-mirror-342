import unittest
import sys, os
from atk_common.http_utils import get_test_response

class TestHttpUtils(unittest.TestCase):

    def test_get_test_response_none(self):
        resp_json = get_test_response(None, 'bo-config-db-api')
        self.assertIsNotNone(resp_json)

if __name__ == "__main__":
    unittest.main()
