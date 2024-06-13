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
# Для воспроизведения аудио файлов будем использовать vlc
import vlc
import time


CHANNELS = 1  # моно
RATE = 16000  # частота дискретизации - кол-во фреймов в секунду
CHUNK = 8000  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам
FORMAT = pyaudio.paInt16 # глубина звука = 16 бит = 2 байта
model = Model("model")

word_friend = 'друг'
# word_hello = ', я слушаю тебя.'
word_hello = ', скажи твою команду.'
word_user_name = 'Люся'

engine = pyttsx3.init()

# Чтобы использовать PyAudio, сначала создаем экземпляр PyAudio, который получит системные ресурсы для PortAudio
py_audio = pyaudio.PyAudio()
stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
rec = KaldiRecognizer(model, 16000)

def play_vlc():
    pass

def say_text(text):
    engine.say(text)
    engine.runAndWait()

def del_word_friend(result_text):
    print('del_word_friend')
    print(type(result_text))
    print('result_text: ДО:',result_text)
    result_text = result_text.replace("\n", "")
    result_text = result_text.replace("partial", "")
    result_text = result_text.replace(":", "")
    result_text = result_text.replace("{", "")
    result_text = result_text.replace("}", "")
    result_text = result_text.replace('"', "")
    print('result_text: ПОСЛЕ:',result_text)
    set_commands = set(result_text.split())
    print('set_commands: ', set_commands)
    return result_text


def listen_to_user():
    # Останавливаем поток, чтобы не попал шум (например приветствие друга) в речь пользователя
    stream.stop_stream()
    # и перезапускаем распознавание, чтобы убрать остатки былых слов
    rec.Reset()

    # *********************************************
    # Проверяем запущен ли плеер и если запущен, то ставим его на паузу
    # if player.is_playing():
    #     player.pause()
    # **********************************************

    # Сначала сообщаем пользователю, что друг услышал, что пользователь позвал друга.
    record_seconds = 2

    listen = True
    max_replay = 1
    count_replay = 0
    result_text = ''
    max_len_rec = 300

    stream.start_stream()
    while listen:
        for _ in range(0, RATE // CHUNK * record_seconds):
            data = stream.read(CHUNK)
            rec.AcceptWaveform(data)

        # Проверяем, изменился текст или нет и если не изменился, то сколько раз он уже не менялся
        if result_text == rec.PartialResult():
            count_replay += 1
            # Если текст не меняется уже max_replay раз
            if count_replay > max_replay - 1:
                listen = False
        elif len(rec.PartialResult()) > max_len_rec:
            listen = False
        else:
            count_replay = 0
            result_text = rec.PartialResult()

    print('*** listen_to_user: result_tex: ', result_text)

    stream.stop_stream()
    rec.Reset()

    return result_text

def look_for_short_command(result_text):

    if 'играй' in result_text:
        print('*** look_for_short_command: Включаю плеер')
        say_text(word_user_name + ', включаю плеер')
        play_vlc()
    else:
        print('*** look_for_short_command:  Команда не распознана')
        say_text('Команда не распознана')
    # ищем и выполняем короткую команду и возвращаемся в main


def process_text_main(result_text):
    if result_text == '':
        print('*** process_text_main: result_text == ''' )
        say_text(word_user_name + word_hello)
        result_text = listen_to_user()

    look_for_short_command(result_text)


def main():
    record_seconds = 2

    say_text('Программа запущена')

    try:
        listen = True
        while listen:
            for _ in range(0, RATE // CHUNK * record_seconds):
                data = stream.read(CHUNK)
                rec.AcceptWaveform(data)

            result_text = rec.PartialResult()

            print('*** main - result_text:', result_text.replace("\n", ""))
            # print('*** main - rec', rec)
            # print('*** main - result_text:', result_text)
            # print('*** main - type(result_text):', type(result_text))

            if word_friend in result_text:
                result_text = del_word_friend(result_text)
                process_text_main(result_text)

            rec.Reset()

    finally:
        print('Программа закрыта')
        py_audio.terminate()


if __name__ == '__main__':
    main()
