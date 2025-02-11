import urllib.request
import json
import os
import time
import sys
from datetime import datetime
from operator import truediv

print('4WATCHAN - Thread Watcher')
print()
print('ctrl+c to exit')
print()
try:
    while True:
        watched_threads = []
        if not os.path.exists('threads.json'):
            print('There are no threads being watched. Exiting...')
            print('Bye.')
            sys.exit()
        else:
            with open('threads.json', 'r') as file:
                watched_threads = json.load(file)

        if len(watched_threads) == 0:
            print('There are no threads being watched. Exiting...')
            print('Bye.')
            sys.exit()

        print(f'{datetime.now().isoformat()} Checking {len(watched_threads)} watched threads')

        updated_threads = []

        for thread_data in watched_threads:
            thread_url = thread_data['url']
            last_checked = int(thread_data['lastChecked'])
            board_code = thread_data['boardCode']
            thread_id = thread_data['threadId']

            data = []
            try:
                with urllib.request.urlopen(thread_url) as url:
                    data = json.load(url)
            except urllib.error.HTTPError as e:
                print('Thread not found -- removing from watchlist')
            except urllib.error.URLError as e:
                print('Malformed thread url -- removing from watchlist')

            if len(data) == 0:
                continue

            posts = data['posts']
            found_new = False
            for post in posts:
                comment_no = post['no']
                if last_checked >= comment_no:
                    continue

                if 'tim' in post and 'ext' in post:
                    found_new = True
                    file_id = post['tim']
                    file_ext = post['ext']
                    file_url = f'https://i.4cdn.org/{board_code}/{file_id}{file_ext}'
                    print(f'{board_code}/{thread_id}/{comment_no} - {file_url}')

                    save_path = f'downloads/{board_code}/{thread_id}/{file_id}{file_ext}'
                    directory = os.path.dirname(save_path)
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    urllib.request.urlretrieve(file_url, save_path)

                thread_data['lastChecked'] = comment_no

            if found_new:
                print()

            updated_threads.append(thread_data)

        with open("threads.json", "w") as file:
            json.dump(updated_threads, file, indent=4)

        time.sleep(5)
except KeyboardInterrupt:
    print('Exiting...')
    print('Bye.')