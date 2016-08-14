from datetime import datetime, timedelta
from django.contrib.auth.models import User

from django.test import TestCase
from tasks import api
from tasks import periods
from tasks.models import Task


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


class TestDailyStats(TestCase):
    def setUp(self):
        self.user = User.objects.create()

        self.period_daily = periods.DAILY
        self.daily_task1 = Task.objects.create(user=self.user, name='Floss', period=self.period_daily)
        self.daily_task2 = Task.objects.create(user=self.user, name='Anki French', period=self.period_daily)

        self.period_weekly = periods.WEEKLY
        self.weekly_task1 = Task.objects.create(user=self.user, name='Gym', period=self.period_weekly)

    def test_find_daily(self):
        api.record_task(self.user, self.daily_task1)
        api.record_task(self.user, self.daily_task2)
        self.assertEqual(2, len(api.load_stats(self.user, self.period_daily)))

    def test_find_daily_only(self):
        api.record_task(self.user, self.daily_task1)
        api.record_task(self.user, self.daily_task2)
        api.record_task(self.user, self.weekly_task1)
        self.assertEqual(2, len(api.load_stats(self.user, self.period_daily)))
