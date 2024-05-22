import sys

# Нужен микрофон. Для этого можно использовать pyaudio.
# Можно использовать SpeechRecognition, который все равно использует pyaudio.
# PyAudio предоставляет Python связь с PortAudio v19 (кроссплатформенной библиотекой ввода-вывода аудио)
# https://people.csail.mit.edu/hubert/pyaudio/docs/
# https://people.csail.mit.edu/hubert/pyaudio/
import pyaudio

# Для распознавания речи используем vosk - автономный API распознавания речи
from vosk import Model, KaldiRecognizer

# Для преобразования текста в речь (для ответов друга) используем pyttsx3
import pyttsx3

CHANNELS = 1  # моно

RATE = 16000  # частота дискретизации - кол-во фреймов в секунду
CHUNK = 8000  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам

FORMAT = pyaudio.paInt16 # глубина звука = 16 бит = 2 байта

RECORD_SECONDS = 2

model = Model("model")

word_friend = 'друг'
word_hello = 'Здравствуй'
word_user_name = 'Люся'

engine = pyttsx3.init()

def voice_to_text(text):
    engine.say(text)
    engine.runAndWait()

def main():

    # Чтобы использовать PyAudio, сначала создаем экземпляр PyAudio, который получит системные ресурсы для PortAudio
    py_audio = pyaudio.PyAudio()

    listen = True
    while listen:
        # Для записи или воспроизведения звука откроем поток на нужном устройстве с нужными параметрами звука
        stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        rec = KaldiRecognizer(model, 16000)

        for ii in range(0, RATE // CHUNK * RECORD_SECONDS):
            data = stream.read(CHUNK)
            rec.AcceptWaveform(data)

        stream.close()
        result_text = rec.PartialResult()
        print(result_text)

        if word_friend in result_text:
            print(word_hello + '' + word_user_name)
            voice_to_text(word_hello + word_user_name)
            listen = False

    py_audio.terminate()

if __name__ == '__main__':
    main()

