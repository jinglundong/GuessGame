import unittest

from service.indicator import Indicator

class TestIndicator(unittest.TestCase):
    def test_right_answer(self):
        indicator = Indicator()

        aligned, not_aligned = indicator.indicate('1234', '1234')

        self.assertEqual(4, aligned)
        self.assertEqual(0, not_aligned)

    def test_completely_wrong_answer(self):
        indicator = Indicator()

        aligned, not_aligned = indicator.indicate('1234', '5678')

        self.assertEqual(0, aligned)
        self.assertEqual(0, not_aligned)

    def test_partially_right_answer(self):
        indicator = Indicator()

        aligned, not_aligned = indicator.indicate('1234', '1478')

        self.assertEqual(1, aligned)
        self.assertEqual(1, not_aligned)
