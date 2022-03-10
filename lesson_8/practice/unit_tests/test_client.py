import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import create_presence, process_ans


class TestClass(unittest.TestCase):
    def test_def_presense(self):
        test = create_presence()
        test[TIME] = 10.00
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 10.00, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_no_response(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})

    def test_200_response(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_400_response(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')


if __name__ == '__main__':
    unittest.main()
