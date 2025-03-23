import unittest
from datetime import timedelta

from dateutil.relativedelta import relativedelta # type: ignore

from pangu.particle.duration.duration import Duration


class TestDuration(unittest.TestCase):

    def test_init(self):
        d = Duration(year=1, day=2, second=30)
        self.assertEqual(d.year, 1)
        self.assertEqual(d.day, 2)
        self.assertEqual(d.second, 30)

    def test_dict(self):
        d = Duration(minute=3)
        self.assertIn("minute", d.dict)
        self.assertEqual(d.dict["minute"], 3)

    def test_base(self):
        d = Duration(hour=1)
        self.assertEqual(d.base, 3600)

    def test_normalize(self):
        d = Duration(second=90)
        d.as_normalize()
        self.assertEqual(d.minute, 1)
        self.assertEqual(d.second, 30)

    def test_add(self):
        d1 = Duration(day=1, hour=2)
        d2 = Duration(hour=1)
        d3 = d1 + d2
        self.assertEqual(d3.hour, 3)
        self.assertEqual(d3.day, 1)

    def test_sub(self):
        d1 = Duration(day=1, hour=3)
        d2 = Duration(hour=1)
        d3 = d1 - d2
        self.assertEqual(d3.hour, 2)

    def test_eq(self):
        d1 = Duration(minute=5)
        d2 = Duration(minute=5)
        self.assertTrue(d1 == d2)

    def test_ne(self):
        d1 = Duration(minute=5)
        d2 = Duration(minute=3)
        self.assertTrue(d1 != d2)

    def test_comparison(self):
        d1 = Duration(second=30)
        d2 = Duration(second=60)
        self.assertTrue(d1 < d2)
        self.assertTrue(d2 > d1)
        self.assertTrue(d1 <= d2)
        self.assertTrue(d2 >= d1)

    def test_radd(self):
        d1 = Duration(second=10)
        result = sum([d1, d1], Duration())
        self.assertEqual(result.second, 20)

    def test_mul(self):
        d = Duration(minute=2)
        result = d * 3
        self.assertEqual(result.minute, 6)

    def test_truediv(self):
        d = Duration(minute=10)
        result = d / 2
        self.assertEqual(result.minute, 5)

    def test_from_dict(self):
        d = Duration.from_dict({"hour": 2, "minute": 30})
        self.assertEqual(d.hour, 2)
        self.assertEqual(d.minute, 30)

    def test_from_timedelta(self):
        td = timedelta(days=2, seconds=3600)
        d = Duration.from_timedelta(td)
        self.assertEqual(d.day, 2)
        self.assertEqual(d.hour, 1)

    def test_from_relativedelta(self):
        rd = relativedelta(years=1, months=2, days=3)
        d = Duration.from_relativedelta(rd)
        self.assertEqual(d.year, 1)
        self.assertEqual(d.month, 2)
        self.assertEqual(d.day, 3)

    def test_describe_basic(self):
        d = Duration(year=1, month=2, day=3, minute=1)
        desc = d.describe(as_text=True)
        self.assertIn("1 year", desc)
        self.assertIn("2 month", desc)
        self.assertIn("3 day", desc)
        self.assertIn("1 minute", desc)

    def test_describe_zero(self):
        d = Duration()
        self.assertEqual(d.describe(as_text=True), "0 second")

    def test_describe_singular_plural(self):
        d = Duration(year=1, month=1, day=1, second=1)
        self.assertEqual(d.describe(as_text=True), "1 year, 1 month, 1 day, 1 second")

        d2 = Duration(year=2, month=3, second=0)
        self.assertEqual(d2.describe(as_text=True), "2 year, 3 month")

    def test_describe_as_dict(self):
        d = Duration(year=1, month=2, day=3)
        desc = d.describe(as_text=False)
        self.assertEqual(desc["year"], 1)
        self.assertEqual(desc["month"], 2)
        self.assertEqual(desc["day"], 3)

    def test_describe_as_dict_zero(self):
        d = Duration()
        desc = d.describe(as_text=False)
        self.assertEqual(desc["second"], 0)
        self.assertEqual(desc["minute"], 0)
        self.assertEqual(desc["hour"], 0)
        self.assertEqual(desc["day"], 0)
        self.assertEqual(desc["month"], 0)
        self.assertEqual(desc["year"], 0)
        self.assertEqual(desc["microsecond"], 0)
        self.assertEqual(desc["week"], 0)

    def test_export(self):
        d = Duration(year=1, month=2, day=3)
        export_data = d.export()
        self.assertEqual(export_data["year"], 1)
        self.assertEqual(export_data["month"], 2)
        self.assertEqual(export_data["day"], 3)
        self.assertEqual(export_data["hour"], 0)
        self.assertEqual(export_data["minute"], 0)

        d2 = Duration.from_dict(export_data)
        self.assertEqual(d2.year, 1)
        self.assertEqual(d2.month, 2)
        self.assertEqual(d2.day, 3)
        self.assertEqual(d2.hour, 0)
        self.assertEqual(d2.minute, 0)


if __name__ == "__main__":
    unittest.main()
