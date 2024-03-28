from pytube import YouTube
from pytube.helpers import safe_filename

video_url = "https://www.youtube.com/watch?v=X-5y1wOw6NQ"
yt = YouTube(video_url)
# yt = YouTube(input('Input URL '))

stream = yt.streams.get_highest_resolution()
output_path = "F:\_Python\YouTube"

dateCreate = yt.publish_date
dateCreateForName = str(dateCreate.year) + '_' + str(dateCreate.month) + '_' + str(dateCreate.day)
author = yt.author
# nameFile = yt.title +  '_' + author + '_' + dateCreateForName + '.' + stream.subtype
nameFileAdd = '_' + author + '_' + dateCreateForName

filename = safe_filename(stream.title)
nameFile = f"{filename}{nameFileAdd}.{stream.subtype}"

stream.download(output_path,nameFile)

print(output_path)
print(yt.title)
print(nameFile)

