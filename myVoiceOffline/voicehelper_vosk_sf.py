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

# для теста playsound3
from playsound3 import playsound


CHANNELS = 1  # моно
RATE = 16000  # частота дискретизации - кол-во фреймов в секунду
CHUNK = 8000  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам
FORMAT = pyaudio.paInt16 # глубина звука = 16 бит = 2 байта
model = Model("model")
# RECORD_SECONDS = 2

word_friend = 'друг'
word_hello = ', я слушаю тебя.'
word_user_name = 'Люся'

engine = pyttsx3.init()

# Чтобы использовать PyAudio, сначала создаем экземпляр PyAudio, который получит системные ресурсы для PortAudio
py_audio = pyaudio.PyAudio()
stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
rec = KaldiRecognizer(model, 16000)

def ps3():
    playsound("vod.mp3", block=False)

def say_text(text):
    engine.say(text)
    engine.runAndWait()
    # print('*** say_text ***:', text)

from just_playback import Playback
def play_just_playback():
    playback = Playback()
    # playback.load_file('test1.mp3')
    playback.load_file('14-shall.mp3')
    # playback.load_file('test_instr.mp3')
    playback.play()
    while playback.playing:
        # *********************************
        stream.start_stream()

        for _ in range(0, RATE // CHUNK * 2):
            data = stream.read(CHUNK)
            rec.AcceptWaveform(data)

        result_text = rec.PartialResult()
        print('*** play_just_playback - result_text:', result_text.replace("\n", ""))

        # Если услышали, что пользователь обращается к другу, то вызываем обработчик, который
        # будет выполнять дальнейшие действия (спрашивать пользователя, запускать другие обработчики)
        if word_friend in result_text:
            rec.Reset()
            print('позвали друга')
            break
        # В противном случае считаем, что пользователь не обращался к другу.
        # Чтобы не копить распознанный текст, очищаем rec
        else:
            print('Что-то сказали')
            rec.Reset()
            # ***********************
       # pass

import vlc
import time
def play_vlc():
    # p = vlc.MediaPlayer('Robertino Loretti - Jamaica.mp4')
    p = vlc.MediaPlayer('14-shall.mp3')
    # p = vlc.MediaPlayer('test1.mp3')
    p.play()

    print('is_playing:', p.is_playing())
    time.sleep(0.1)
    # a = input()
    print('is_playing:', p.is_playing())

    # while p.is_playing():
    #     pass

def working_with_commands():
    """ Обработка указаний пользователя"""

    # Останавливаем поток, чтобы не попал шум (например приветствие друга) в речь пользователя
    stream.stop_stream()
    # и перезапускаем распознавание, чтобы убрать остатки былых слов
    rec.Reset()
    # Сначала сообщаем пользователю, что друг услышал, что пользователь позвал друга.
    say_text(word_user_name + word_hello)
    print('*** working_with_commands - say_text:', word_user_name + word_hello)

    # Время одной порции слов делаем уже побольше (3 сек), чем когда просто ждали когда позовут друга (2сек)
    record_seconds = 3

    listen = True

    # Неизвестно сколько времени понадобится пользователю, чтобы дать указание другу, поэтому будем слушать
    # до тех пор, пока текст указания result_text не меняется max_replay раз.
    # Для этого считаем количество повторений count_replay распознанного текста
    max_replay = 0
    count_replay = 0
    result_text = ''

    # Также перестаем слушать, когда текст указания слишком длинный (может быть пользователь просто поет)
    max_len_rec = 300

    # Слушаем что говорит пользователь. Это может быть длинное предложение,
    # поэтому слушаем, пока пользователь не сделает длинную паузу или предложение не будет слишком длинным
    stream.start_stream()
    while listen:
        # Обрабатываем порцию за record_seconds секунд
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

    print('*** working_with_commands - result_text:', count_replay, len(rec.PartialResult()),len(result_text),
          result_text.replace("\n", ""))

    # Все услышали, поэтому останавливаем поток и перезапускаем распознание
    stream.stop_stream()
    rec.Reset

    # Переходим к обработке услышанного
    if 'играй' in result_text:
        print('*** working_with_commands - обработка указаний пользователя: Включаю плеер')
        say_text(word_user_name + ', включаю плеер')
        # ps3()
        # play_just_playback()
        play_vlc()
    elif 'найди' in result_text:
        print('*** working_with_commands - обработка указаний пользователя:  Ищу')
        say_text('Ищу')
    elif 'добавь' in result_text:
        print('*** working_with_commands - обработка указаний пользователя:  Добавляю')
        say_text('Добавляю')
    elif 'удали' in result_text:
        print('*** working_with_commands - обработка указаний пользователя:  Удаляю')
        say_text('Удаляю')
    elif 'Прощай' in result_text:
        print('*** working_with_commands - обработка указаний пользователя:  Прощай')
        say_text('До встречи')
    else:
        print('*** working_with_commands - обработка указаний пользователя:  Команда не распознана')
        say_text('Команда не распознана')

    stream.start_stream()
    rec.Reset()

def main():
    # Ждем обращение пользователя к другу, т.е. ждем, когда пользователь скажет слово друг,
    # для этого достаточно 2 секунд.
    # 1 секунды мало, так как в этом случае возможно частое попадание слова друг на границу секунды
    # 3 секунды много, так как получаются значительные паузы в реакции друга
    record_seconds = 2

    say_text('Программа запущена')


    # Слушаем постоянно.
    # Здесь поток не стопим, так как важно услышать слово друг, шумы не важны,
    # но может быть друг из соседнего потока.
    # Но распознание перезапускаем, чтобы не копилось
    try:
        listen = True
        while listen:
            # Обрабатываем порцию за record_seconds секунд
            for _ in range(0, RATE // CHUNK * record_seconds):
                data = stream.read(CHUNK)
                rec.AcceptWaveform(data)

            result_text = rec.PartialResult()

            print('*** main - result_text:', result_text.replace("\n", ""))

            # Если услышали, что пользователь обращается к другу, то вызываем обработчик, который
            # будет выполнять дальнейшие действия (спрашивать пользователя, запускать другие обработчики)
            if word_friend in result_text:
                # stream.stop_stream()
                rec.Reset()
                working_with_commands()
                # stream.start_stream()
            # В противном случае считаем, что пользователь не обращался к другу.
            # Чтобы не копить распознанный текст, очищаем rec
            else:
                # stream.stop_stream()
                rec.Reset()

    finally:
        print('Closing programm Ok')
        py_audio.terminate()

if __name__ == '__main__':
    main()

