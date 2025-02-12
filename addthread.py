import json
import os

WATCHLIST_FILE = 'threads.json'
def load_watchlist():
    """Loads the watchlist from a JSON file or initializes an empty list."""
    if not os.path.exists(WATCHLIST_FILE):
        return []
    try:
        with open(WATCHLIST_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Warning: Watchlist is malformed. Initializing a new one.")
        return []

def save_watchlist(watchlist):
    """Saves the updated watchlist to the JSON file."""
    with open(WATCHLIST_FILE, 'w', encoding='utf-8') as file:
        json.dump(watchlist, file, indent=4)

def normalize_url(url):
    """Extracts and formats the necessary thread information from a given URL."""
    url = url.replace('http://', '').replace('https://', '').split('#')[0]
    parts = url.split('/')

    if len(parts) < 4:
        print("Error: Invalid thread URL format.")
        return None, None

    # return boardcode, threadid
    return parts[1], parts[3]


def add_thread_to_watchlist():
    """Handles user input and adds a new thread to the watchlist if valid."""
    watchlist = load_watchlist()

    orig_url = input("Enter thread URL to add to watchlist: ").strip()
    board_code, thread_id = normalize_url(orig_url)

    if not board_code or not thread_id:
        print("Failed to add thread. Please enter a valid URL.")
        return

    thread_url = f"https://a.4cdn.org/{board_code}/thread/{thread_id}.json"

    if any(thread['threadId'] == thread_id and thread['boardCode'] == board_code for thread in watchlist):
        print(f"Thread `{thread_id}` is already in the watchlist.")
        return

    watchlist.append({
        'url': thread_url,
        'lastChecked': '0',
        'boardCode': board_code,
        'threadId': thread_id
    })

    save_watchlist(watchlist)

    print(f"Thread `{thread_id}` added to watchlist successfully.")
    print("Run `watcher.py` to monitor your threads.")


if __name__ == "__main__":
    print(' _   ___  _     _  _______  _______  _______  __   __  _______  __    _ ')
    print('| | |   || | _ | ||   _   ||       ||       ||  | |  ||   _   ||  |  | |')
    print('| |_|   || || || ||  |_|  ||_     _||       ||  |_|  ||  |_|  ||   |_| |')
    print('|       ||       ||       |  |   |  |       ||       ||       ||       |')
    print('|___    ||       ||       |  |   |  |      _||       ||       ||  _    |')
    print('    |   ||   _   ||   _   |  |   |  |     |_ |   _   ||   _   || | |   |')
    print('    |___||__| |__||__| |__|  |___|  |_______||__| |__||__| |__||_|  |__|')
    print()
    add_thread_to_watchlist()
