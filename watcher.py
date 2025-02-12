import urllib.request
import json
import os
import time
import sys
from datetime import datetime

WATCHLIST_FILE = 'threads.json'
DOWNLOADS_DIR = 'downloads'
CHECK_INTERVAL = 30  # seconds between checks

def load_watchlist():
    """Loads the watchlist from a JSON file or exits if no threads are being watched."""
    if not os.path.exists(WATCHLIST_FILE):
        print("No threads are being watched. Exiting...")
        sys.exit()
    try:
        with open(WATCHLIST_FILE, 'r', encoding='utf-8') as file:
            watchlist = json.load(file)
            if not watchlist:
                print("No threads are being watched. Exiting...")
                sys.exit()
            return watchlist
    except (json.JSONDecodeError, IOError):
        print("Watchlist is malformed. Exiting...")
        sys.exit()

def save_watchlist(threads):
    """Saves watchlist file"""
    with open(WATCHLIST_FILE, "w", encoding='utf-8') as file:
        json.dump(threads, file, indent=4)

def fetch_thread_data(thread_url):
    """Fetches thread JSON data from the given URL, handling errors gracefully."""
    try:
        with urllib.request.urlopen(thread_url) as url:
            return json.load(url)
    except urllib.error.HTTPError:
        print(f"Thread not found: {thread_url} -- Removing from watchlist")
    except urllib.error.URLError:
        print(f"Malformed URL: {thread_url} -- Removing from watchlist")
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from: {thread_url} -- Skipping")
    return None

def download_file(board_code, thread_id, file_id, file_ext):
    """Downloads an image file from 4chan and saves it in the appropriate directory."""
    file_url = f"https://i.4cdn.org/{board_code}/{file_id}{file_ext}"
    save_path = os.path.join(DOWNLOADS_DIR, board_code, thread_id, f"{file_id}{file_ext}")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        urllib.request.urlretrieve(file_url, save_path)
        print(f"Downloaded: {board_code}/{thread_id}/{file_id}{file_ext}")
    except Exception as e:
        print(f"Failed to download {file_url}: {e}")

def check_threads():
    """Checks watched threads for new images and updates the watchlist."""
    print(' _   ___  _     _  _______  _______  _______  __   __  _______  __    _ ')
    print('| | |   || | _ | ||   _   ||       ||       ||  | |  ||   _   ||  |  | |')
    print('| |_|   || || || ||  |_|  ||_     _||       ||  |_|  ||  |_|  ||   |_| |')
    print('|       ||       ||       |  |   |  |       ||       ||       ||       |')
    print('|___    ||       ||       |  |   |  |      _||       ||       ||  _    |')
    print('    |   ||   _   ||   _   |  |   |  |     |_ |   _   ||   _   || | |   |')
    print('    |___||__| |__||__| |__|  |___|  |_______||__| |__||__| |__||_|  |__|')
    print()
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            watchlist = load_watchlist()
            updated_threads = []

            print(f"{datetime.now().isoformat()} - Checking {len(watchlist)} watched thread/s")

            for thread in watchlist:
                thread_url = thread['url']
                last_checked = int(thread['lastChecked'])
                board_code = thread['boardCode']
                thread_id = thread['threadId']

                data = fetch_thread_data(thread_url)
                if not data:
                    continue # Skip if data couldn't be retrieved

                found_new = False
                for post in data.get('posts', []):
                    comment_no = post['no']
                    if last_checked >= comment_no:
                        continue # Skip if no new media

                    if 'tim' in post and 'ext' in post:
                        found_new = True
                        download_file(board_code, thread_id, post['tim'], post['ext'])

                    thread['lastChecked'] = comment_no

                if found_new:
                    print()

                updated_threads.append(thread)

            # Save updated watchlist
            save_watchlist(updated_threads)

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nExiting... Bye!")

if __name__ == "__main__":
    check_threads()