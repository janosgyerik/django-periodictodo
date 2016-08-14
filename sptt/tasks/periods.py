from datetime import datetime, timedelta
import abc


CHOICES = (
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
)


class Period:
    @abc.abstractmethod
    def get_start(self):
        raise NotImplementedError

    def _date(self, date):
        return date if date else datetime.now()


class DailyPeriod(Period):
    def get_start(self, date=None):
        return self._date(date).replace(hour=0, minute=0, second=0, microsecond=0)


class WeeklyPeriod(Period):
    def get_start(self, date=None):
        days_to_start = timedelta(days=date.weekday())
        return self._date(date).replace(hour=0, minute=0, second=0, microsecond=0) - days_to_start

DAILY = DailyPeriod()
WEEKLY = WeeklyPeriod()
