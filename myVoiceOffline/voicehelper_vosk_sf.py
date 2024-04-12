import sys

import pyaudio
import vosk

# нужен микрофон
# Можно использовать pyaudio, можно использовать SpeechRecognition, который все равно использует pyaudio

# https://people.csail.mit.edu/hubert/pyaudio/docs/
# https://people.csail.mit.edu/hubert/pyaudio/

# CHANNELS = 1 if sys.platform == 'darwin' else 2 # darwin это macOS https://docs.python.org/3/library/sys.html#module-sys
#                     # Такие параметры указаны на people.csail Но для win c CHANNELS=2 не работает, работает с 1
CHANNELS = 1  # моно

# RATE = 44100  # частота дискретизации - кол-во фреймов в секунду
# CHUNK = 1024  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам
RATE = 16000  # частота дискретизации - кол-во фреймов в секунду
# CHUNK = 16000  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам
CHUNK = 8000  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам
# RATE = 44100, CHUNK = 1024 такие параметры в people.csail, но с ними не распознает
# RATE = 16000, CHUNK = 8000 распознает лучше, чем RATE = 16000, CHUNK = 16000

FORMAT = pyaudio.paInt16 # глубина звука = 16 бит = 2 байта

RECORD_SECONDS = 5

model = vosk.Model("model")
rec = vosk.KaldiRecognizer(model, 16000)

# Чтобы использовать PyAudio, сначала создаем экземпляр PyAudio, который получит системные ресурсы для PortAudio
py_audio = pyaudio.PyAudio()

# Для записи или воспроизведения звука откроем поток на нужном устройстве с нужными параметрами звука
# stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print('Recording...')

for ii in range(0, RATE // CHUNK * RECORD_SECONDS):
    data = stream.read(CHUNK)
    rec.AcceptWaveform(data)
    # print(ii)
    # print(rec.PartialResult())

print(rec.PartialResult())

# # PartialResult распознает лучше всех
# print("rec.PartialResult()")
# print(rec.PartialResult())
# print(end="\n\n")
# print("rec.Result()")
# print(rec.Result())
# print(end="\n\n")
# print("rec.FinalResult()")
# print(rec.FinalResult())

stream.close()
py_audio.terminate()

