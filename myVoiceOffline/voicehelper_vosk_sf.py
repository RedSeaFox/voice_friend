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
RECORD_SECONDS = 2

word_friend = 'друг'
word_hello = ', я слушаю тебя.'
word_user_name = 'Люся'

engine = pyttsx3.init()

# Чтобы использовать PyAudio, сначала создаем экземпляр PyAudio, который получит системные ресурсы для PortAudio
py_audio = pyaudio.PyAudio()
stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
rec = KaldiRecognizer(model, 16000)

def say_text(text):
    engine.say(text)
    engine.runAndWait()


def working_with_commands():
    say_text(word_user_name + word_hello)
    print(word_user_name + word_hello)

    record_seconds = 3

    listen = True

    result_text = ''
    count_replay = 0

    rec.Reset()
    # Слушаем что говорит пользователь. Это может быть длинное предложение,
    # поэтому слушаем, пока пользователь не сделает длинную паузу или предложение не будет слишком длинным
    while listen:

        for _ in range(0, RATE // CHUNK * record_seconds):
            data = stream.read(CHUNK)
            rec.AcceptWaveform(data)

        if result_text == rec.PartialResult():
            count_replay += 1
            if count_replay > 2:
                listen = False
        else:
            result_text = rec.PartialResult()
            print(result_text)

    # Обрабатываем команду
    if 'играй' in result_text:
        print(word_user_name + ', включаю плеер')
        say_text(word_user_name + ', включаю плеер')

def main():
    try:
        say_text('Программа запущена')

        listen = True
        while listen:
            # rec = KaldiRecognizer(model, 16000)
            # rec.Reset()

            for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                data = stream.read(CHUNK)
                rec.AcceptWaveform(data)

            result_text = rec.PartialResult()
            print(result_text)

            if word_friend in result_text:
                rec.Reset()
                working_with_commands()

            rec.Reset()

    finally:
        print('Closing programm Ok')
        py_audio.terminate()

if __name__ == '__main__':
    main()

