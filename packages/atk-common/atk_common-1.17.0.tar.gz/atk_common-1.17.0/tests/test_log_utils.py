import unittest
import sys, os
from atk_common.log_utils import add_log_item

class TestLogUtils(unittest.TestCase):
    
    def test_add_log_item(self):
        add_log_item("Test message")

if __name__ == "__main__":
    unittest.main()
