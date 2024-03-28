import os
from pytube import YouTube

'''Иммитация скачивания mp3
На самом деле кодек на выходе получается другой, например aac и расширение у скачанного файла mp4
Это можно проверить так: ffmpeg.exe -i 'ИмяСкачанногоФайла.extFile'
и посмотреть в блоке stream - audio
Т.е. сначала скачивается только аудиодорожка, а потом у скачанного файла расширение меняется на .mp3
'''

path_save = "F:\_Python\YouTube"
url = "https://www.youtube.com/watch?v=X-5y1wOw6NQ"

yt = YouTube(url)

#Download mp3
audio_file = yt.streams.filter(only_audio=True).first().download(path_save)
base, ext = os.path.splitext(audio_file)
new_file = base + '.mp3'
os.rename(audio_file, new_file)
#
# #Download Video
# ys = yt.streams.filter(res="1080p").first()
# ys.download(PATH_SAVE)