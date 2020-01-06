#!/usr/bin/env python3

import requests


# Load the playlist
STATUS_OK = 200
base_url = "https://api.deezer.com/playlist/"
playlist_id = "204500701"
tracks_req = "/tracks?index=0&limit={}"

r = requests.get(base_url + playlist_id)

if r.status_code != STATUS_OK:
    print("Status code: {}".format(r.status_code))

data = r.json()

nb_tracks = data['nb_tracks']
print("Title: {}".format(data['title']))
print("Description: {}".format(data['description']))
print("Nbr tracks: {}".format(nb_tracks))

songs = None

if len(data['tracks']['data']) == nb_tracks:
    songs = data['tracks']['data']
else:
    # By default, loads only 400 songs. To load everything, should use an other
    # kind of request
    r = requests.get(base_url + playlist_id + tracks_req.format(nb_tracks))
    songs = r.json()['data']


# Save the playlist
f = open("out/playlist.csv", "w+")
f.write("Title,Artist,Album,Duration,Time added, Id song, Id artist, Id album\n")

for song in songs:
    f.write("\"{}\",\"{}\",\"{}\",{},{},{},{},{}\n".format(song['title'], song['artist']['name'], song['album']['title'],
        song['duration'], song['time_add'], song['id'], song['artist']['id'], song['album']['id']))

f.close()