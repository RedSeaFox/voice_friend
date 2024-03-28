from datetime import datetime as dt
from pytube import Playlist, YouTube
from pytube.helpers import safe_filename

print(dt.now())

play_list_url = "https://www.youtube.com/playlist?list=PLUHJylAlRLXcgXC4aIOR9pPuq-DpHlj6z"
path_save = "F:\_Python\YouTube"

play_list = Playlist(play_list_url)


for url in play_list.video_urls:
    print(url)
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()

    dateCreate = yt.publish_date
    dateCreateForName = str(dateCreate.year) + '_' + str(dateCreate.month) + '_' + str(dateCreate.day)
    author = yt.author
    # nameFile = yt.title +  '_' + author + '_' + dateCreateForName + '.' + stream.subtype
    nameFileAdd = '_' + author + '_' + dateCreateForName

    filename = safe_filename(stream.title)
    nameFile = f"{filename}{nameFileAdd}.{stream.subtype}"
    print(nameFile)

    stream.download(path_save,nameFile)

print(dt.now())

