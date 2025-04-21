import unittest
import sys, os
from atk_common.docker_utils import get_image_version, list_all_images

class TestDockerUtils(unittest.TestCase):

    def test_get_image_version_none(self):
        ver = get_image_version()
        self.assertIsNone(ver)

    def test_get_image_version_not_none_1(self):
        ver = get_image_version('bo-config-db-api')
        self.assertIsNotNone(ver)

    def test_get_image_version_not_none_2(self):
        ver = get_image_version('bo-case-web')
        self.assertIsNotNone(ver)

if __name__ == "__main__":
    unittest.main()
