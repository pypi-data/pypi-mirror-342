import os
import unittest

from dotenv import load_dotenv
from daspython.auth.authenticate import DasAuth

class TestAuth(unittest.TestCase):
    def test_authenticate(self):    
        load_dotenv()
        auth = DasAuth(os.getenv("DAS_URL"), os.getenv("DAS_USERNAME"), os.getenv("DAS_PASSWORD"))
        success = auth.authenticate(os.getenv("CHECK_HTTPS").lower() == 'true')
        self.assertEqual(success, True,f'Success should be True but got {success}.')
        
if __name__ == '__main__':
    unittest.main()

