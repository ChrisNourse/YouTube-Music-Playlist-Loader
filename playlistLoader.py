import csv
import logging
from ytmusicapi import YTMusic
from urllib.parse import urlparse, parse_qs

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Authenticate using the headers_auth.json you obtained during setup
ytmusic = YTMusic('oauth.json')
logging.info("Authenticated with YouTube Music.")

# Specify the existing playlist URL here
playlist_url = ""

if not playlist_url:
    playlist_url = input("Please enter the playlist URL: ")

# List to store songs that failed to load
failed_songs = []

# Read songs from CSV
songs_data = []
with open('songs.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        songs_data.append({
            'artist': row['Artist'],
            'song': row['Song']
        })
logging.info(f"Read {len(songs_data)} songs from the CSV.")

# Extract playlist ID from the URL
parsed_url = urlparse(playlist_url)
query_params = parse_qs(parsed_url.query)
playlist_id = query_params.get('list', [None])[0]
if not playlist_id:
    logging.error("Could not extract playlist ID from the provided URL.")
    exit(1)  # Exit the script if playlist ID is not found
logging.info(f"Target playlist ID is {playlist_id}.")


# Fetch the current songs in the playlist
try:
    playlist_contents = ytmusic.get_playlist(playlist_id, limit=5000)  # Assuming max 5000 songs in a playlist
    existing_songs = {item['title']: item['videoId'] for item in playlist_contents['tracks']}
except Exception as e:
    logging.error(f"Failed to fetch the playlist with ID {playlist_id}. Ensure the playlist exists and you have access to it.")
    logging.error(str(e))
    exit(1)


# Add songs to the specified playlist
for data in songs_data:
    search_query = f"{data['artist']} - {data['song']}"
    logging.info(f"Searching for {search_query}.")
    
    search_results = ytmusic.search(search_query, filter="songs")

    
    if search_results:
        # Check if the artist in search results matches the original artist
        result_artist = search_results[0].get('artists', [{}])[0].get('name', "")
        if result_artist.lower() == data['artist'].lower():
            song_id = search_results[0]['videoId']
            
            if song_id in existing_songs.values():
                logging.info(f"{search_query} is already in the play11list.")
                continue

            ytmusic.add_playlist_items(playlist_id, [song_id])
            logging.info(f"Added {search_query} to the playlist.")
        else:
            logging.warning(f"Artist mismatch for: {search_query}. Found: {result_artist}")
            # Prompt user for action
            print(f"\nMismatch for search: {search_query}")
            for idx, result in enumerate(search_results, 1):
                print(f"{idx}. {result['title']} by {result.get('artists', [{}])[0].get('name', '')}")
            print(f"{len(search_results) + 1}. Skip song")
            
            # Get user choice
            choice = 0
            while choice < 1 or choice > len(search_results) + 1:
                try:
                    choice = int(input("Choose an option (1 - n): "))
                except ValueError:
                    continue
            
            if choice <= len(search_results):
                song_id = search_results[choice-1]['videoId']
                ytmusic.add_playlist_items(playlist_id, [song_id])
                logging.info(f"Added {search_results[choice-1]['title']} to the playlist based on user selection.")
            else:
                failed_songs.append(search_query)
    else:
        logging.warning(f"Couldn't find: {search_query}")
        failed_songs.append(search_query)


if failed_songs:
    logging.info("The following songs failed to load properly:")
    for song in failed_songs:
        logging.info(song)
else:
    logging.info("All songs loaded properly.")
    
logging.info("Script execution completed.")
