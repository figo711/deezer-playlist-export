#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Small script to export Deezer playlists to CSV files

    Author: Corentin Chauvin-Hameau
    Date: 2020
    License: The Unlicense
"""

import requests
import tkinter as tk
from tkinter import filedialog


#*************************
#**  Playlist loading  ***
#*************************
def load_playlist(playlist_id):
    STATUS_OK = 200
    base_url = "https://api.deezer.com/playlist/"
    playlist_id = str(playlist_id)
    tracks_req = "/tracks?index=0&limit={}"

    r = requests.get(base_url + playlist_id)

    if r.status_code != STATUS_OK:
        print("Status code: {}".format(r.status_code))
        return None

    data = r.json()

    nb_tracks = data['nb_tracks']
    songs = None

    if len(data['tracks']['data']) == nb_tracks:
        songs = data['tracks']['data']
    else:
        # By default, loads only 400 songs. To load everything, should use an other
        # kind of request
        r = requests.get(base_url + playlist_id + tracks_req.format(nb_tracks))
        songs = r.json()['data']


    # Create a string of tracks
    s = "Title,Artist,Album,Duration,Time added,Id song,Id artist,Id album\n\n"

    for song in songs:
        s += "\"{}\",\"{}\",\"{}\",{},{},{},{},{}\n".format(song['title'], song['artist']['name'], song['album']['title'],
            song['duration'], song['time_add'], song['id'], song['artist']['id'], song['album']['id'])

    return data, s

#**********************
#**  GUI callbacks  ***
#**********************
tracks_string = None

def load_cb():
    global text_field, playlist_name_lbl, nb_tracks_lbl
    global tracks_string

    data, tracks_string = load_playlist(playlist_id_txt.get())

    if data is not None:
        playlist_name_lbl.config(text="Playlist name: {}     ".format(data['title']))
        nb_tracks_lbl.config(text="Nbr tracks: {}".format(data['nb_tracks']))

        text_field.delete('1.0', tk.END)
        text_field.insert(tk.END, tracks_string)


def save_cb():
    global tracks_string

    filename = filedialog.asksaveasfilename(initialdir = "/home", title = "Select file", filetypes = (("csv","*.csv"), ("text","*.txt"),("all files","*.*")))
    print("f", filename)

    if filename is not None:
        f = open(filename, 'w+', encoding='utf-8')
        f.write(tracks_string)
        f.close()


#**************************
#**  GUI configuration  ***
#**************************

# Window and frames config
window = tk.Tk()
window.title("Playlist exporter")
window.geometry('500x300')

top_frame = tk.Frame(window)
mid_frame = tk.Frame(window)
bot_frame = tk.Frame(window)

top_frame.pack(fill=tk.X)
mid_frame.pack(fill=tk.X)
bot_frame.pack(fill=tk.BOTH)

# Top frame
playlist_id_lbl = tk.Label(top_frame, text="Playlist id: ")
playlist_id_lbl.pack(side=tk.LEFT)

playlist_id_txt = tk.Entry(top_frame, width=15)
playlist_id_txt.pack(side=tk.LEFT)

load_btn = tk.Button(top_frame, text="Load", command=load_cb)
load_btn.pack(side=tk.LEFT)

save_btn = tk.Button(top_frame, text="Save", command=save_cb)
save_btn.pack(side=tk.LEFT)

# Mid frame
playlist_name_lbl = tk.Label(mid_frame, text="Playlist name:       ")
playlist_name_lbl.pack(side=tk.LEFT)

nb_tracks_lbl = tk.Label(mid_frame, text="Nbr tracks: ")
nb_tracks_lbl.pack(side=tk.LEFT)

# Bot frame
scrollbar = tk.Scrollbar(bot_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_field = tk.Text(bot_frame, height=1000, width=300)
text_field.pack(side=tk.LEFT, fill=tk.Y)
scrollbar.config(command=text_field.yview)
text_field.config(yscrollcommand=scrollbar.set)

# Main loop
window.mainloop()
