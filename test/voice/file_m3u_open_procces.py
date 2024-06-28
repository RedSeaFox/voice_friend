import os.path
import time
import vlc

# playlist_m3u = open('list.m3u')
# playlist_m3u = open('pl_yt.m3u')
playlist_m3u = open('8941.m3u')
print('playlist_m3u:', playlist_m3u.__sizeof__())

print(time.time())

playlist_list = playlist_m3u.readlines()

print('playlist_list:', playlist_list.__sizeof__())

print(time.time())

list_for_tuple = list()

for line in playlist_list:
    if line[0] == '#':
        continue
    elif line[0:5] == 'file:':
        list_for_tuple.append(os.path.abspath(line[8:]))
    elif line[0:6] == 'https:':
        # list_for_tuple.append(os.path.abspath(line))
        list_for_tuple.append(line.rstrip())

playlist_in_tuple = tuple(list_for_tuple)
print(time.time())

print('list_for_tuple.__sizeof__:', list_for_tuple.__sizeof__())
print('len list_for_tuple:', len(list_for_tuple))
print('playlist_in_tuple.__sizeof__:', playlist_in_tuple.__sizeof__())
print('len playlist_in_tuple:', len(playlist_in_tuple))

player = vlc.Instance()

media_player = player.media_list_player_new()

media_list = player.media_list_new()

for song in list_for_tuple:
    media_list.add_media(song.rstrip())

media_player.set_media_list(media_list)

media_player.play()

time.sleep(8)