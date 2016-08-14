from datetime import datetime, timedelta
import abc


CHOICES = (
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
)


class Period:
    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_start(self):
        raise NotImplementedError

    def _date(self, date):
        return date if date else datetime.now()


class DailyPeriod(Period):
    @property
    def name(self):
        return 'daily'

    def get_start(self, date=None):
        return self._date(date).replace(hour=0, minute=0, second=0, microsecond=0)


class WeeklyPeriod(Period):
    @property
    def name(self):
        return 'weekly'

    def get_start(self, date=None):
        date = self._date(date)
        days_to_start = timedelta(days=date.weekday())
        return date.replace(hour=0, minute=0, second=0, microsecond=0) - days_to_start

DAILY = DailyPeriod()
WEEKLY = WeeklyPeriod()
