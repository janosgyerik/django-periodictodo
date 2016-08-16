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


class TestDailyProgress(TestCase):
    def setUp(self):
        self.user = User.objects.create()

        self.period = periods.DAILY
        self.task1 = Task.objects.create(user=self.user, name='Floss', period=self.period.name, count=2)
        self.task2 = Task.objects.create(user=self.user, name='Anki French', period=self.period.name)

        self.other_period_task = Task.objects.create(user=self.user, name='Gym', period=periods.WEEKLY)

    def test_find_period(self):
        api.record_task(self.user, self.task1)
        api.record_task(self.user, self.task2)
        self.assertEqual(2, len(api.load_progress(self.user, self.period)))

    def test_find_only_specific_period(self):
        api.record_task(self.user, self.task1)
        api.record_task(self.user, self.task2)
        api.record_task(self.user, self.other_period_task)
        self.assertEqual(2, len(api.load_progress(self.user, self.period)))

    def test_find_grouped_by_task(self):
        api.record_task(self.user, self.task1)
        api.record_task(self.user, self.task1)
        api.record_task(self.user, self.task2)
        self.assertEqual(2, len(api.load_progress(self.user, self.period)))

    def test_none_completed(self):
        progress = api.load_progress(self.user, self.period)
        self.assertEqual(0, progress[0].count)
        self.assertEqual(0, progress[1].count)

    def test_half_completed(self):
        api.record_task(self.user, self.task1)
        progress = api.load_progress(self.user, self.period)
        self.assertEqual(1, progress[0].count)
        self.assertEqual(0, progress[1].count)

    def test_completed(self):
        api.record_task(self.user, self.task1)
        api.record_task(self.user, self.task1)
        progress = api.load_progress(self.user, self.period)
        self.assertEqual(2, progress[0].count)
        self.assertEqual(0, progress[1].count)

    def test_completed_with_interleaved_task(self):
        api.record_task(self.user, self.task1)
        api.record_task(self.user, self.task2)
        api.record_task(self.user, self.task1)
        progress = api.load_progress(self.user, self.period)
        self.assertEqual(2, progress[0].count)
        self.assertEqual(1, progress[1].count)

    def test_ok_to_exceed_target_count(self):
        api.record_task(self.user, self.task1)
        api.record_task(self.user, self.task1)
        api.record_task(self.user, self.task1)
        progress = api.load_progress(self.user, self.period)
        self.assertEqual(3, progress[0].count)
        self.assertEqual(0, progress[1].count)
