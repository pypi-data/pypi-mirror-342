import unittest
import sys, os
from atk_common.docker_utils import get_current_container_info

class TestDockerUtils(unittest.TestCase):

    def test_get_container_info(self):
        info = get_current_container_info()
        self.assertIsNone(info)

if __name__ == "__main__":
    unittest.main()
