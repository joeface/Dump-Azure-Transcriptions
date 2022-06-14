import json
from os import path
from pprint import pprint
import requests
from time import sleep

from dotenv import dotenv_values


DATA = []
TRASCRIPTION_ITERATION = 0


def fetch():

    global DATA

    config = dotenv_values()

    if not config or not 'REGION' in config or not 'KEY' in config or not 'ID' in config:
        exit("Please provide API Region, Key and Transcription ID in .env")

    list_iteration = 0
    next_url = f"https://{config['REGION']}.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/{config['ID']}/files?skip=0&top=100"
    while next_url:
        print(f'\nFetching List {next_url}')
        r = requests.get(next_url, timeout=60, headers={
                         'Ocp-Apim-Subscription-Key': config['KEY']})
        if r.status_code != requests.codes.ok:
            print(f"! Error fetching {next_url}")
            return None

        response_data = r.json()

        if response_data and 'values' in response_data:
            if path.isdir('cache'):
                list_file = open(f"cache/list-{list_iteration}.json", "w")
                json.dump(response_data, list_file, ensure_ascii=False)

            parse(response_data)

        if '@nextLink' in response_data:
            next_url = response_data['@nextLink']
            list_iteration += 1
            sleep(2)

        else:
            next_url = None

    json_file = open("dump.json", "w")
    json.dump(DATA, json_file, ensure_ascii=False)
    print(f"\nDone\nTotal Records: {len(DATA)}")


def fetch_transcription(url):

    r = requests.get(url, timeout=60)

    if r.status_code != requests.codes.ok:
        print(f"! Error fetching transcription {url}")
        return None

    return r.json()


def parse(response):

    global DATA, TRASCRIPTION_ITERATION
    for v in response['values']:

        if v['properties']['size'] > 300:

            # Ignore short calls

            obj = {
                'name': v['name'],
                'size': v['properties']['size'],
                'content': ''
            }

            t = fetch_transcription(v['links']['contentUrl'])

            if t and 'combinedRecognizedPhrases' in t and len(t['combinedRecognizedPhrases']) > 0:
                obj['content'] = t['combinedRecognizedPhrases'][0]['display']

                DATA.append(obj)

                if path.isdir('cache'):
                    t_file = open(
                        f"cache/transcription-{TRASCRIPTION_ITERATION}.json", "w")
                    json.dump(t, t_file, ensure_ascii=False)

            TRASCRIPTION_ITERATION += 1


fetch()
