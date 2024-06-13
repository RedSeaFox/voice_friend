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
# RECORD_SECONDS = 2

word_friend = 'друг'
word_hello = ', я слушаю тебя.'
word_user_name = 'Люся'

engine = pyttsx3.init()

# Чтобы использовать PyAudio, сначала создаем экземпляр PyAudio, который получит системные ресурсы для PortAudio
py_audio = pyaudio.PyAudio()
stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
rec = KaldiRecognizer(model, 16000)


# ****************************************
player = vlc.MediaPlayer()
# player.

paused = vlc.State().Paused
print('paused: ', paused)

# ****************************************


def say_text(text):
    engine.say(text)
    engine.runAndWait()


def play_vlc():
    # p = vlc.MediaPlayer('14-shall.mp3')
    #
    # p.play()
    # time.sleep(0.1)
    #
    # # print('p.retain():  ', p.retain())
    # print('p.is_playing():', p.is_playing())
    # print('vlc.MediaPlayer().is_playing():', vlc.MediaPlayer().is_playing())
    # print('p.can_pause():', p.can_pause())
    # print('vlc.MediaPlayer().can_pause():', vlc.MediaPlayer().can_pause())
    #
    # print('p.get_instance: ', p.get_instance)
    # print('p.get_media:     ', p.get_media)


    # *******************************************


    if player.get_state() == vlc.State(4):
        player.pause()
    else:
        # creating a new media
        # media = vlc.Media("test1.mp3")
        # media = vlc.Media("14-shall.mp3")
        media = vlc.Media("vod.mp3")
        # media = player.media_new("test1.mp3")

        player.set_media(media)

        # start playing video
        player.play()

        # wait so the video can be played for 5 seconds
        # irrespective for length of video
        time.sleep(0.1)

    # *******************************************

def working_with_commands():
    """ Обработка указаний пользователя"""
    # Останавливаем поток, чтобы не попал шум (например приветствие друга) в речь пользователя
    stream.stop_stream()
    # и перезапускаем распознавание, чтобы убрать остатки былых слов
    rec.Reset()

    # *********************************************
    # Проверяем запущен ли плеер и если запущен, то ставим его на паузу
    print('player.get_state():  ', player.get_state())
    print('player.retain():  ', player.retain())
    print('is_playing:', player.is_playing())

    if player.is_playing():
        player.pause()
    # elif player.get_state() = vlc.State(4):
    # elif player.get_state() == vlc.State(4):
    #     player.pause()


    # **********************************************


    # Сначала сообщаем пользователю, что друг услышал, что пользователь позвал друга.
    say_text(word_user_name + word_hello)
    print('*** working_with_commands - say_text:', word_user_name + word_hello)

    # Время одной порции слов делаем уже побольше (3 сек), чем когда просто ждали когда позовут друга (2сек)
    # record_seconds = 3
    record_seconds = 2

    listen = True

    # Неизвестно сколько времени понадобится пользователю, чтобы дать указание другу, поэтому будем слушать
    # до тех пор, пока текст указания result_text не меняется max_replay раз.
    # Для этого считаем количество повторений count_replay распознанного текста
    # max_replay = 0
    # max_replay = 2
    max_replay = 1
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

        print('in while listen count_replay = ', count_replay, '  rec.PartialResult() = ', rec.PartialResult())

        # Проверяем, изменился текст или нет и если не изменился, то сколько раз он уже не менялся
        if result_text == rec.PartialResult():
            count_replay += 1
            # Если текст не меняется уже max_replay раз
            if count_replay > max_replay -   1:
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
                rec.Reset()
                working_with_commands()
            # В противном случае считаем, что пользователь не обращался к другу.
            # Чтобы не копить распознанный текст, очищаем rec
            else:
                rec.Reset()

    finally:
        print('Closing programm Ok')
        py_audio.terminate()

if __name__ == '__main__':
    main()

