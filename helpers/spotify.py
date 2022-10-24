import os
import requests
import json

user_id = "r3xit"
spotify_url = "https://api.spotify.com/v1/users/{}/playlists"
create_token = "BQC-xaNqA0kggNeTKtEbwtqi6EOGP4C9LeFLgVmFCNUEPOR8HggBrBKW3JDqu3FBpocrwsNFLRFf1ogbzhQGgrefp1MNDnsTLnqIRrWhP3Gd5JkXhR7H0G8DYpQcktkYF549s88pkYDmTakyFVfyVIGA6eyAYEzwnQMalP1FVkwRLdG5meZAaFlJk1bvfTklWEvoMj_ZOJG6l19QBAKxp3Hx49Y46rstUQ"
add_item = "BQBqhbydOzb8LCkQjpLFHQm7jSf3DwthImkVSwYS9M10MRwPicA0BgnwMHfYUOiBKtEYFAtDlIcs9FzBpHGEmrtYW9IzFVbyzYqv5XMytb7FOoafgPgUjY_gJnzD7rU-jPZNfs1jdhVw6BNnM3-ADn_9cx1gEvzSsf7iYKxOgkdJa8S1m6iStVcbzsD7NTYKl9yR_HSlbTVdBD-Y5_5JoElVIO9iDflSZA"

def create_playlist(name, public):
    spotify_id = spotify_url.format(user_id)
    response = requests.post(spotify_id, headers={
        "Authorization": f"Bearer {create_token}"},
        json = {"name" : name, "public": public
        })

    json_response = response.json()
    print(json_response)
    return json_response



def get_playlist_id(resp):
    id = resp["id"]
    return id



def add_song_to_playlist(playlist_url, songs_info):

    uris = [info["spotify_uri"] for song, info in songs_info.items()]
    request_body = json.dumps({
        "uris": uris
    })
    request_data = json.dumps(uris)

    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_url)

    response = requests.post(query, data= request_data, headers= {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(add_item)
    })

    print(response.status_code)
    response_json = response.json()
    return response_json