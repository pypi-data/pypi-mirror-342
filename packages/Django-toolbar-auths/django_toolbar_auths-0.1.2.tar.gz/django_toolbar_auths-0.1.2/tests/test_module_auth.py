
import unittest
from Django_auths.module_auth import hello

class TestHelloFunction(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello("World"), "Hello, World!")

if __name__ == '__main__':
    unittest.main()