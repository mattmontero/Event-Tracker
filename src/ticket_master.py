"""
countryCode=US
dmaId=382
keyword=San Jose Sharks
segmentId=KZFzniwnSyZfZ7v7nE        <- Sports
genreId=KnvZfZ7vAdI                 <- Hockey
subGenreId=KZazBEonSMnZfZ7vFEE      <- NHL
"""

import os
import sys
import time

import requests
import slack

sys.path.append(os.path.abspath("./"))
from src.event import Event

# Ticket Master Constants
API_KEY = os.getenv("TICKET_MASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2"
EVENTS_URL = f"{BASE_URL}/events.json"

WARRIORS = {
    "params": {
        "keyword": "Golden State Warriors",
        "dmaId": "382",
    }
}

SHARKS = {
    "price": 40,
    "params": {
        "keyword": "Sharks",
        "dmaId": "382",
        "genreId": "KnvZfZ7vAdI",
        "subGenreId": "KZazBEonSMnZfZ7vFEE",
    }
}

TEAMS = {
    "sharks": SHARKS,
    "warriors": WARRIORS
}

# Slack Constants
SLACK_TOKEN = os.getenv("SLACK_TOKEN")


def events(params: dict):
    params["apikey"] = API_KEY
    response = requests.get(url=EVENTS_URL, params=params)
    if response:
        return response.json()
    return None


def parse_events(events):
    event_list = []
    if events:
        for event in events['_embedded']['events']:
            name = dates = priceRanges = event_id = None
            if 'name' in event:
                name = event['name']

            if 'dates' in event:
                dates = event['dates']

            if 'priceRanges' in event:
                priceRanges = event['priceRanges'][0]

            if 'id' in event:
                event_id = event['id']

            if None not in [name, dates, priceRanges, event_id]:
                print(f"Adding {name}")
                event_list.append(Event(event_id, name, priceRanges, dates))
    return event_list


def filter_by_price(events, price):
    filtered = []
    for event in events:
        if event.min_price < price:
            filtered.append(event)
    return filtered


def notify(events, channel):
    client = slack.WebClient(token=SLACK_TOKEN)
    if len(events) == 0:
        client.chat_postMessage(
            channel=f"#{channel}",
            text="No events. Error?"
        )
    else:
        message = ""
        for event in events:
            message += event.slack_str() + "\n"
        client.chat_postMessage(
            channel=f"#{channel}",
            text=message
        )


if __name__ == "__main__":
    for index, (team, params) in enumerate(TEAMS.items()):
        events_response = events(params['params'])
        clean_events = parse_events(events_response)
        if "price" in params:
            clean_events = filter_by_price(clean_events, params['price'])

        clean_events.sort(key=lambda tEvent: tEvent.date)
        notify(clean_events, team)
