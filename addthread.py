import json
import os

print('4WATCHAN - Thread Adder')

watched_threads = []
if not os.path.exists('threads.json'):
    with open('threads.json', 'w') as file:
        json.dump(watched_threads, file, indent=4)
else:
    with open('threads.json', 'r') as file:
        watched_threads = json.load(file)

orig_url = input('Enter thread url to watch: ')
orig_url = orig_url.replace('http://', '').replace('https://', '')
orig_url = orig_url.split('#')[0]
board_code = orig_url.split('/')[1]
thread_id = orig_url.split('/')[3]

thread_url = f'https://a.4cdn.org/{board_code}/thread/{thread_id}.json'
watched_threads.append({
    'url': thread_url,
    'lastChecked': '0',
    'boardCode': board_code,
    'threadId': thread_id
})

with open('threads.json', 'w') as file:
    json.dump(watched_threads, file, indent=4)
