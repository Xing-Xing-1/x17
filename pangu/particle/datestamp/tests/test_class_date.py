import unittest
from pangu.particle.datestamp.date import Date
from pangu.particle.datestamp.time import Time
from pangu.particle.duration import Duration

class TestDate(unittest.TestCase):

    def test_init_and_repr(self):
        d = Date(2025, 3, 24)
        self.assertEqual(d.year, 2025)
        self.assertEqual(d.month, 3)
        self.assertEqual(d.day, 24)
        self.assertIn("Date(year=2025", repr(d))

    def test_today(self):
        today = Date.today()
        self.assertIsInstance(today, Date)

    def test_add_duration(self):
        d = Date(2025, 3, 24)
        result = d + Duration(day=3)
        self.assertIsInstance(result, Date)
        self.assertEqual(result.day, 27)

    def test_sub_duration(self):
        d = Date(2025, 3, 24)
        result = d - Duration(day=4)
        self.assertEqual(result.day, 20)

    def test_sub_date(self):
        d1 = Date(2025, 3, 30)
        d2 = Date(2025, 3, 25)
        diff = d1 - d2
        self.assertIsInstance(diff, Duration)
        self.assertEqual(diff.day, 5)

    def test_invalid_add(self):
        d = Date(2025, 3, 24)
        with self.assertRaises(TypeError):
            _ = d + 123

    def test_combine_with_time(self):
        d = Date(2025, 3, 24)
        t = Time(14, 30)
        combined = d.combine(t)
        self.assertEqual(combined.year, 2025)
        self.assertEqual(combined.hour, 14)