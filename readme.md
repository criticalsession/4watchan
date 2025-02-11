# 4WATCHAN - Thread Watcher and Downloader

4WATCHAN is a simple Python project that lets you watch threads on 4chan for new images and videos and automatically download them. The project consists of two scripts:

- **`addthread.py`**: Adds a thread URL to a watch list.
- **`watcher.py`**: Monitors the added threads for new posts and downloads any new images/videos from them.

## Features

- **Add Threads**: Easily add thread URLs to your watch list.
- **Automatic Monitoring**: Regularly checks for new posts in the threads.
- **Image/Webm Downloading**: Downloads new images and videos from posts automatically.
- **Organized Storage**: Saves images in a structured folder hierarchy based on board and thread.

## Requirements

- **Python 3.x**

## Getting Started

1. **Clone or Download the Repository**

Clone the repository or simply download the two Python scripts (`addthread.py` and `watcher.py`) to your local machine.

   ```bash
   git clone https://github.com/criticalsession/4watchan.git
   cd 4watchan
   ```

2. **Add a Thread to Watch**

Run the `addthread.py` script to add a new thread URL to your watch list.

```bash
python addthread.py
```

- You will be prompted to enter a thread URL.
- The script processes the URL, extracts the board code and thread ID, and then adds it to the threads.json file.

3. **Start Watching Threads**

Run the `watcher.py` script to begin monitoring the threads listed in `threads.json`:

```bash
python watcher.py
```

- The script will periodically (every 20 seconds) check each thread for new posts.
- If new posts with images/videos are found, the images/videos will be downloaded into the appropriate folder (`downloads/<boardCode>/<threadId>/`).
- Watcher automatically removes any 404'd threads from the thread watch list

## Todo

- [ ] Adjust interval through flag
- [ ] Better logging

## Known Issues

**Basic URL parsing**: The current URL processing is simple, so ensure your input URL matches the expected format:
- `https://boards.4chan.org/<boardcode>/thread/<thread_id>`, or
- `https://boards.4chan.org/<boardcode>/thread/<thread_id>#p<comment_id>`