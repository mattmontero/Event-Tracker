

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
        return self._dates['start']['localDate']

    @property
    def priceRange(self):
        return self._priceRange

    @property
    def min_price(self):
        return self._priceRange['min']

    def slack_str(self):
        message = ""
        if self.min_price < 20:
            message += "@here"
        return f"{message} {self.date} - {self._name} - *${self.min_price}*"
