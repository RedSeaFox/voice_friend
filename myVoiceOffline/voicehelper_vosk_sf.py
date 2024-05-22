import sys

# Нужен микрофон. Для этого можно использовать pyaudio.
# Можно использовать SpeechRecognition, который все равно использует pyaudio.
# PyAudio предоставляет Python связь с PortAudio v19 (кроссплатформенной библиотекой ввода-вывода аудио)
# https://people.csail.mit.edu/hubert/pyaudio/docs/
# https://people.csail.mit.edu/hubert/pyaudio/
import pyaudio

# Для распознавания речи используем vosk - автономный API распознавания речи
import vosk

# Для преобразования текста в речь (для ответов друга) используем pyttsx3
import pyttsx3

CHANNELS = 1  # моно
# CHANNELS = 1 if sys.platform == 'darwin' else 2
# darwin это macOS https://docs.python.org/3/library/sys.html#module-sys
# Такие параметры указаны на people.csail Но для win c CHANNELS=2 не работает, работает с 1

RATE = 16000  # частота дискретизации - кол-во фреймов в секунду
# RATE = 44100  # частота дискретизации - кол-во фреймов в секунду
CHUNK = 8000  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам
# CHUNK = 1024  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам

# RATE = 44100, CHUNK = 1024 такие параметры в people.csail, но с ними не распознает
# RATE = 16000, CHUNK = 8000 распознает лучше, чем RATE = 16000, CHUNK = 16000

FORMAT = pyaudio.paInt16 # глубина звука = 16 бит = 2 байта

RECORD_SECONDS = 2

model = vosk.Model("model")

word_friend = 'друг'
worf_hello = 'Здравствуй'
word_user_name = 'Люся'

engine = pyttsx3.init()

def voice_to_text(text):
    engine.say(text)
    engine.runAndWait()

def main():

    # Чтобы использовать PyAudio, сначала создаем экземпляр PyAudio, который получит системные ресурсы для PortAudio
    py_audio = pyaudio.PyAudio()

    # for i in range(5):
    listen = True
    while listen:
        # Для записи или воспроизведения звука откроем поток на нужном устройстве с нужными параметрами звука
        stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        rec = vosk.KaldiRecognizer(model, 16000)

        print('Recording...')

        for ii in range(0, RATE // CHUNK * RECORD_SECONDS):
            data = stream.read(CHUNK)
            rec.AcceptWaveform(data)
            # print(ii)
            # print(rec.PartialResult())

        # print(rec.PartialResult())
        # # PartialResult распознает лучше всех
        # print(rec.PartialResult())
        # print(rec.Result())
        # print(rec.FinalResult())

        stream.close()
        result_text = rec.PartialResult()
        # print(rec.PartialResult())
        print(result_text)

        if word_friend in result_text:
            print(worf_hello + word_user_name)
            voice_to_text(worf_hello + word_user_name)
            # break


    py_audio.terminate()

if __name__ == '__main__':
    main()

