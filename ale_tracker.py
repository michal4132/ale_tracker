#!/usr/bin/env python3
from prettytable import PrettyTable
from datetime import datetime, timezone
import requests
import json
import time
import sys

if len(sys.argv) < 2:
    print("No parcel number")
    sys.exit(1)

parcels = []
for parcel in sys.argv[1:]:
    parcels.append(parcel)

def get_status(parcel):
    url = "https://edge.allegro.pl/logistics/carriers/ALLEGRO/waybills/{}/history".format(parcel)

    headers = {
        "Accept": "application/vnd.allegro.public.v1+json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15"
    }

    response = requests.get(url, headers=headers)
    return response.text

def convert_date(date):
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    date = date.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return date.strftime("%d %b %Y, %H:%M")

def print_dashboard(data):
    tab = PrettyTable(["Parcel", "Date", "Last status"])
    tab.align = "l"

    for parcel in data:
        parcel_data = json.loads(data[parcel])
        date = convert_date(parcel_data["history"][-1]["date"])
        tab.add_row([parcel, date, parcel_data["history"][-1]["description"]])
    print(tab)

def print_parcel_history(data):
    json_data = json.loads(data)

    tab = PrettyTable(['Date', 'Status'])
    tab.align = "l"
    for status in json_data["history"]:
        tab.add_row([convert_date(status["date"]), status["description"]])
    print(tab)

parcels_data = {}
if (len(parcels) == 1):
    data = get_status(parcels[0])
    print_parcel_history(data)
else:
    for parcel in parcels:
        data = get_status(parcel)
        parcels_data.update({parcel: data})
    print_dashboard(parcels_data)

