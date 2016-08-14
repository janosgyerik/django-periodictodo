from django.test import TestCase
from tasks import periods
from datetime import datetime, timedelta


class TestPeriod(TestCase):
    def test_period_interface_cannot_be_used_directly(self):
        self.assertRaises(NotImplementedError, periods.Period().get_start)


class TestDailyPeriod(TestCase):
    def test_start_at_period_start(self):
        date = datetime(2016, 8, 14)
        self.assertEqual(date, periods.DailyPeriod().get_start(date))

    def test_start_at_period_middle(self):
        date = datetime(2016, 8, 14)
        self.assertEqual(date, periods.DailyPeriod().get_start(date + timedelta(hours=1)))


class TestWeeklyPeriod(TestCase):
    def test_start_at_period_start(self):
        date = datetime(2016, 8, 8)
        self.assertEqual(date, periods.WeeklyPeriod().get_start(date))

    def test_start_at_period_middle(self):
        date = datetime(2016, 8, 8)
        self.assertEqual(date, periods.WeeklyPeriod().get_start(date + timedelta(days=1)))
