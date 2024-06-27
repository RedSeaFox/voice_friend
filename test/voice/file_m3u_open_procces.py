import os.path
import time
import vlc

playlist_m3u = open('list.m3u')
# playlist_m3u = open('8941.m3u')
print('playlist_m3u:', playlist_m3u.__sizeof__())

print(time.time())

playlist_list = playlist_m3u.readlines()

print('playlist_list:', playlist_list.__sizeof__())

print(time.time())

list_for_tuple = list()

for line in playlist_list:
    if line[0] == '#':
        continue
    list_for_tuple.append(os.path.abspath(line[8:]))

playlist_in_tuple = tuple(list_for_tuple)
print(time.time())

print('list_for_tuple:', list_for_tuple.__sizeof__())
print('playlist_in_tuple:', playlist_in_tuple.__sizeof__())

player = vlc.Instance()

media_player = player.media_list_player_new()

media_list = player.media_list_new()

for song in list_for_tuple:
    media_list.add_media(song.rstrip())

media_player.set_media_list(media_list)

media_player.play()

time.sleep(8)