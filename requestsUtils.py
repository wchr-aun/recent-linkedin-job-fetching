import time

import requests

import config


def requests_with_retry(requestsFn, attempt=3):
    for i in range(attempt):
        try:
            response = requestsFn()
            if response.status_code == 200:
                return response
            else:
                print(f"Attempt {i + 1}: Request failed with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {i + 1}: Request failed: {e}")

        delay = config.getDelayGapInSecond() * i
        print(f"Retrying in {delay} seconds...")
        time.sleep(delay)
