import unittest

import tartempion


class TartempionTest(unittest.TestCase):
    def test_tartempion_loaded(self):
        self.assertTrue(tartempion)
