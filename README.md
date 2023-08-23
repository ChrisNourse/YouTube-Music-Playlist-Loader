
# YouTube Music Playlist Updater

This script allows you to automatically add songs from a CSV file to a YouTube Music playlist.

## Prerequisites

- Python 3.7+
- [Poetry](https://python-poetry.org/docs/) for dependency management

## Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/ChrisNourse/YouTube-Music-Playlist-Loader.git
    ```

2. **Set up the Python environment with Poetry**
    ```bash
    poetry install
    ```

### `oauth.json`

To use the `ytmusicapi`, you'll need to authenticate via a `oauth.json` file. 

To generate `oauth.json`, follow the instructions on the ytmusic documentation:  
https://ytmusicapi.readthedocs.io/en/stable/setup/index.html

### `songs.csv`

The CSV file should be formatted as follows:

```
Artist,Song
Queen,Bohemian Rhapsody
The Beatles,Let It Be
... and so on
```

Ensure there are no extra spaces or lines.

## Usage

1. Prepare your `songs.csv` as described above.
2. Run the script:
   ```bash
   playlistLoader.py
   ```

3. If you haven't provided a playlist URL in the code, you will be prompted to enter it when you run the script.
4. The script will read songs from the CSV, search for them on YouTube Music, and add them to the specified playlist.
    - If there's an artist mismatch, you'll be prompted to choose among the search results or skip the song.

## Notes

- The script checks if a song is already in the playlist before attempting to add it.
- Ensure you handle the `oauth.json` with care, as it contains sensitive data.


## Acknowledgments

This project utilized [OpenAI's ChatGPT](https://openai.com/research/publications/chatgpt-chat-done-right/) for assistance in generating portions of the code and documentation. Special thanks to the OpenAI team for their contributions to the AI community.
