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
model = Model("model")
RECORD_SECONDS = 3

word_friend = 'друг'
word_hello = ', я слушаю тебя.'
word_user_name = 'Люся'

engine = pyttsx3.init()

# Чтобы использовать PyAudio, сначала создаем экземпляр PyAudio, который получит системные ресурсы для PortAudio
py_audio = pyaudio.PyAudio()
stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

def say_text(text):
    engine.say(text)
    engine.runAndWait()


def working_with_commands():
    rec = KaldiRecognizer(model, 16000)

    print(word_user_name + word_hello)
    say_text(word_user_name + word_hello)

    for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        data = stream.read(CHUNK)
        rec.AcceptWaveform(data)

    result_text = rec.PartialResult()
    print(result_text)

    if 'играй' in result_text:
        print(word_user_name + ', включаю плеер')
        say_text(word_user_name + ', включаю плеер')

def main():
    try:
        # say_text('Программа запущена')

        listen = True
        while listen:
            rec = KaldiRecognizer(model, 16000)

            for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                data = stream.read(CHUNK)
                rec.AcceptWaveform(data)

            result_text = rec.PartialResult()
            print(result_text)

            if word_friend in result_text:
                working_with_commands()
    finally:
        print('Closing programm Ok')
        py_audio.terminate()

if __name__ == '__main__':
    main()

