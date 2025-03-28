import unittest
from pangu.particle.datestamp.time import Time
from pangu.particle.duration import Duration

class TestTime(unittest.TestCase):

    def test_init_and_repr(self):
        t = Time(14, 30)
        self.assertEqual(t.hour, 14)
        self.assertEqual(t.minute, 30)
        self.assertIn("Time(hour=14", repr(t))

    def test_now(self):
        now = Time.now()
        self.assertIsInstance(now, Time)

    def test_add_duration(self):
        t = Time(14, 0)
        result = t + Duration(minute=30)
        self.assertIsInstance(result, Time)
        self.assertEqual(result.minute, 30)

    def test_sub_duration(self):
        t = Time(14, 30)
        result = t - Duration(minute=15)
        self.assertEqual(result.minute, 15)

    def test_sub_time(self):
        t1 = Time(15, 0)
        t2 = Time(14, 0)
        diff = t1 - t2
        self.assertEqual(diff.hour, 1)

    def test_invalid_add(self):
        t = Time(14)
        with self.assertRaises(TypeError):
            _ = t + 123