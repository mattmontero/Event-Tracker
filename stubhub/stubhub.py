import logging
import os
import sys
import time

import requests
import slack

sys.path.append(os.path.abspath("./"))
from api import get_events
from event import Event

# Slack Constants
SLACK_TOKEN = os.getenv("SLACK_TOKEN")

def determine_category(event):
    if 'ancestors' in event and 'categories' in event['ancestors']:
        for category in event['ancestors']['categories']:
            if category['name'] in ['Sports', 'Hockey', 'Basketball']:
                return 'Sports'
        return "Event"
    return "not_found"

def parse_events(events):
    if "events" in events:
        event_list = []
        for event in events['events']:
            # category = determine_category(event)
            event_id = event['id']
            event_name = event['name']
            price_range = event['ticketInfo']
            dates = event['eventDateLocal']
            event_list.append(Event(event_id, event_name, price_range, dates))
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


def get_channels():
    client = slack.WebClient(token=SLACK_TOKEN)
    channels_list = client.channels_list(exclude_archived=1)
    excluded_channels = ['eventtracker', 'random', 'general']
    return_channels = []
    if hasattr(channels_list, 'data') and 'channels' in channels_list.data:
        for channel in channels_list.data['channels']:
            if channel['name'] not in excluded_channels:
                return_channels.append((channel['name'], channel['topic']['value']))
    return return_channels


if __name__ == "__main__":
    # We will use the channel name as keyword to search stubhub api.
    channels = get_channels()

    for channel, topic in channels:
        keyword = channel.replace("_", " ")
        params = {}
        if topic:
            try:
                params.update(eval(topic))
            except Exception:
                pass

        raw_events_response = get_events(keyword, params)
        parsed_events = parse_events(raw_events_response)
        parsed_events.sort(key=lambda tEvent: tEvent.date)
        notify(parsed_events, channel)
