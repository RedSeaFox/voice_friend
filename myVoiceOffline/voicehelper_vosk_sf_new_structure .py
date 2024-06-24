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
word_hello = ', скажи твою команду.'
word_user_name = 'Люся'

engine = pyttsx3.init()

# Чтобы использовать PyAudio, сначала создаем экземпляр PyAudio, который получит
# системные ресурсы для PortAudio (короче подключаемся к микрофону)
py_audio = pyaudio.PyAudio()
# Открываем поток для чтения (input=True) данных с микрофона по-умолчанию и задаем параметры
stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
rec = KaldiRecognizer(model, 16000)

# Большинство команд к другу касаются плеера vlc, поэтому он должен быть всегда доступен
media_player = vlc.MediaListPlayer()

def play_vlc():
    # Если плеер уже запущен, но находится в состоянии пауза, то запускаем его (продолжаем играть)
    if media_player.get_state() == vlc.State(4):
        media_player.pause()
    else:
        # Если плеер еще не запущен - запускаем
        player = media_player.get_instance()
        media = player.media_new("vod.mp3")
        media_list = player.media_list_new()
        media_list.add_media(media)
        media_player.set_media_list(media_list)

        media_player.play()

        time.sleep(0.1)


def say_text(text):
    engine.say(text)
    engine.runAndWait()


def listen_to_user():
    # Останавливаем поток, чтобы не попал шум (например приветствие друга) в речь пользователя
    stream.stop_stream()
    # и перезапускаем распознавание, чтобы убрать остатки былых слов
    rec.Reset()

    # Сначала сообщаем пользователю, что друг услышал, что пользователь позвал друга.
    record_seconds = 2

    listen = True
    max_replay = 1
    count_replay = 0
    result_text = ''
    max_len_rec = 100

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

    print('listen_to_user: result_tex: ', result_text.replace("\n", ""))

    rec.Reset()

    return result_text

def look_for_short_command(set_commands):
    set_play = {'играй', 'играть', 'пой', 'петь'}
    set_seek = {'найди', 'ищи', 'поиск', 'найти'}

    # ищем и выполняем короткую команду
    if not set_commands:
        say_text(word_user_name + ', я не услышал команду. Обратись опять к другу')
        print('look_for_short_command: я не услышал команду. Обратись опять к другу')
    elif not set_commands.isdisjoint(set_play):
        # if 'играй' in result_text:
        print('look_for_short_command: Включаю плеер')
        say_text(word_user_name + ', включаю плеер')
        play_vlc()
    elif not set_commands.isdisjoint(set_seek):
        set_commands -= set_seek
        print('look_for_short_command: Ищу', set_commands)
        say_text(word_user_name + ', ищу ' +  ' '.join(set_commands))
    else:
        # ни одна из коротких команд (играй, найди, назад, вперед, время и проч) не найдена =>
        # значит ждем когда пользователь опять обратится к другу
        say_text(word_user_name + ', я не смог распознать команду. Обратись опять к другу')
        print('look_for_short_command: я не смог распознать команду. Обратись опять к другу')
     # и возвращаемся в main
    # stream.stop_stream()
    rec.Reset()
    # stream.start_stream()


def process_text_main(set_commands):
    # print('process_text_main: result_text в начале', result_text)
    # set_commands_user = commands_user_to_set(result_text)
    # print('process_text_main: result_text после перевода в set', result_text)
    set_commands -= {'друг'}
    print('process_text_main: set_commands_user:', set_commands)

    if not set_commands: # если множество пустое
        # Останавливаем поток, чтобы не попал шум (например приветствие друга) в речь пользователя
        # stream.stop_stream()
        # и перезапускаем распознавание, чтобы убрать остатки былых слов
        rec.Reset()
        # stream.start_stream()
        print('process_text_main: set_commands_user пустое' )
        print('process_text_main:  ', word_user_name , word_hello )
        say_text(word_user_name + word_hello)
        result_text = listen_to_user()
        print('process_text_main: result_text', result_text.replace("\n", ""))
        set_commands = commands_to_set(result_text)

    look_for_short_command(set_commands)

def commands_user_to_set(result_text):
    # print('commands_user_to_set: result_text:',result_text.replace("\n", ""))
    # result_text = result_text[result_text.find('друг')+4:]
    # print('после удаления друг', result_text)
    result_text = result_text.replace("\n", "")
    result_text = result_text.replace("partial", "")
    result_text = result_text.replace(":", "")
    result_text = result_text.replace("{", "")
    result_text = result_text.replace("}", "")
    result_text = result_text.replace('"', "")
    # result_text = result_text[result_text.find('друг')+4:]

    print('commands_user_to_set: result_text после удаления служебных символов:', result_text)

    set_commands_user = set(result_text.split())
    print('commands_user_to_set: set_commands_user: ', set_commands_user)

    return set_commands_user


def commands_to_set(result_text):
    result_text = result_text.replace("\n", "")
    result_text = result_text.replace("partial", "")
    result_text = result_text.replace(":", "")
    result_text = result_text.replace("{", "")
    result_text = result_text.replace("}", "")
    result_text = result_text.replace('"', "")

    set_commands = set(result_text.split())

    return set_commands


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

            print('main: result_text 1 :', result_text.replace("\n", ""))
            # print('main: result_text 2 :', ' ' + result_text.replace("\n", "") + ' ')
            # print('main: result_text 3 :', result_text)
            # print('main: result_text 4 :', ' ' + result_text + ' ')

            # set_main = main_to_set(result_text)

            # print(set_main)

            # if word_friend in result_text:
            if word_friend in result_text:
                set_commands = commands_to_set(result_text)
                if word_friend in set_commands:
                    # Как только услышали слово друг, останавливаем плеер, если он включен
                    if media_player.is_playing():
                        media_player.pause()

                    print('main: обнаружено слово друг')
                    # process_text_main(result_text)
                    process_text_main(set_commands)
            # else:
            #     print('main: rec.Reset()')
            #     rec.Reset()
            print('main: rec.Reset()')
            rec.Reset()
            result_text = ''
            stream.stop_stream()
            stream.start_stream()
    finally:
        stream.stop_stream()
        stream.close()
        py_audio.terminate()
        print('Программа закрыта')


if __name__ == '__main__':
    main()
