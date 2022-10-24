from contextlib import nullcontext
from operator import ne
from urllib import response
import requests
import googleapiclient.discovery as gapic

songs_info = {} # Dictionary that contains songs information

youtubeApi_key = "AIzaSyB72GUz0aBnN2HrxaIAmc1EOroQC91aoJc"
search_item = "BQDTQVD7dwpv1jBM7OybSZSL4sKihbeBDDHiWZMzvElVthwFA2C84zbtb_0DH1ppdEjfpxuS0FA02YYFQtnTqv_p2lbXIUBCru1Wk_NIeMPg2LJDDhnMi9buWDO5e5OsgutbAwnKxiH4_TFxYMX5E9_9dpYpFhcQdM7m"

youtube = gapic.build('youtube', 'v3', developerKey=youtubeApi_key)

def extract_title_and_artist(video_title, video_channel):
    artist = ''
    title = ''

    # Extracting artist and title from text

    # If - is in the title, it will be split
    if '-' in video_title:
        s = str(video_title).split('-')
        artist = s[0]
        title = s[1]

    # If : is in the title, it will be split
    elif ':' in video_title:
        s = str(video_title).split(':')
        artist = s[0]
        title = s[1]

    # If – is in the title, it will be split
    elif '–' in video_title:
        s = str(video_title).split('–')
        artist = s[0]
        title = s[1]

    # If the title does not have dashes or colon, probably the video_title is only the song name,
    # For the artist the program must search the channel name, which will probably be the artist's name
    else:
        title = video_title
        artist_channel = str(video_channel)
        temp = artist_channel.split('-')
        artist = temp[0]

    if ',' in artist:
        s = artist.split(', ')
        split_artist = s[0]
    else:
        split_artist = artist

    counter = 0
    # If a parenthesis is inside the title, the text after the parenthesis is not counted
    for letter in title:
        if letter == '(':
            split_title = title[0:(counter - 1)]
            break

        elif letter == '[':
            split_title = title[0:(counter - 1)]
            break

        else:
            split_title = title

        counter += 1

    return {'artist' : split_artist.strip(), 'track' : split_title.strip()}


def get_spotify_uri(song_name, artist):
    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0".format(song_name, artist)

    response = requests.get(query, headers = {
        "Content-type":"application/json",
        "Authorization":"Bearer {}".format(search_item)
    })

    response_json = response.json()


    songs = response_json["tracks"]["items"]

    # Using only the first song
    try:
        uri = songs[0]["uri"]

    except IndexError:

        uri = 'null'

    return uri

def initiate_youtube(playlist_url):
    nextPageToken = None
    counter = 0

    while True:

        playlist_request = youtube.playlistItems().list(

            part = "content Details",

            playlistId = playlist_url,

            maxResults = 50,

            pageToken = nextPageToken

        )

        playlist_response = playlist_request.execute()

        nextPageToken = playlist_response.get("nextPageToken")

        videos_ids = []

        for item in playlist_response["items"]:
            videos_ids.append(item["contentDetails"]["videoId"])

        video_request = youtube.videos().list(
            part = "snippet",
            id = ",".join(videos_ids)
        )

        video_response = video_request.execute()

        for item in video_response["items"]:

            video_title = item["snippet"]["title"]

            video_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            video_channel = item["snippet"]["channelTitle"]

            try:
                video_info = extract_title_and_artist(video_title, video_channel)

                song_name = video_info['track']

                artist = video_info['artist']

                spotify_uri = get_spotify_uri(song_name, artist)

                if (spotify_uri!='null'):
                    songs_info[video_title] = {"video_url" : video_url, "song_name": song_name, "spotify_uri": spotify_uri}
                    counter += 1
                    print(f"{counter}: {artist} - {song_name} succesfully transferred")
            except KeyError as e:
                print("Song details unavailable")

        if not nextPageToken:
            break

    print(f"total songs tranferred: {len(songs_info)}")
    return songs_info

def length(songs_info):
    length = len(songs_info)
    return length
