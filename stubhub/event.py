import calendar
from datetime import datetime

class Event:
    """ Event """
    def __init__(self, event_id: str, name: str, priceRange: dict, dates: dict):
        self._event_id = event_id
        self._name = name
        self._priceRange = priceRange
        self._dates = dates

    def __str__(self):
        return f"{self.date} - {self._name} - *${self.min_price}*"

    @property
    def event_id(self):
        return self._event_id

    @property
    def name(self):
        return self._name

    @property
    def date(self):
        return self._dates[:10]

    @property
    def priceRange(self):
        return self._priceRange

    @property
    def min_price(self):
        return self._priceRange['minListPrice']

    def date_details(self):
        dt = datetime.strptime(self.date, "%Y-%m-%d")
        day = calendar.day_name[dt.weekday()]
        time = self._dates[11:16]
        return f"{self.date} {day} {time}"

    def slack_str(self):
        message = ""
        if self.min_price < 20:
            message += ":moneybag:"
        date_details = self.date_details()
        return f"{message} {date_details} - {self._name} - *${self.min_price}*"
