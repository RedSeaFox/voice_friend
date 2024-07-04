import os.path
import time
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


CHANNELS = 1  # моно
RATE = 16000  # частота дискретизации - кол-во фреймов в секунду
CHUNK = 8000  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам
FORMAT = pyaudio.paInt16  # глубина звука = 16 бит = 2 байта
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

# Большинство команд к другу касаются плеера, поэтому он должен быть всегда доступен
vlc_instance = vlc.Instance()
# media_list_player = vlc.MediaListPlayer()
media_list_player = vlc_instance.media_list_player_new()


def load_playlist(playlist_name: str):
    playlist_list = list()

    print('load_playlist() : Начало составления списка', time.time())

    try:
        # playlist_m3u = open('my_playlist.m3u', encoding='utf-8')
        playlist_m3u = open(playlist_name, encoding='utf-8')
        playlist_list_from_m3u = playlist_m3u.readlines()

    except FileNotFoundError:
        say_text('load_playlist: Плейлист не найден. Воспроизведение не возможно')
        return playlist_list

    except Exception:
        say_text('load_playlist: Плейлист не загружен. Неизвестная ошибка. Обратитесь к разработчику')
        return playlist_list

    for line in playlist_list_from_m3u:
        if line[0] == '#':
            continue
        elif line[0:5] == 'file:':
            # playlist_list.append(os.path.abspath(line[8:]))
            media_path = os.path.abspath(line[8:].rstrip())
            if os.path.isfile(media_path):
                playlist_list.append(media_path)
        elif line[0:6] == 'https:':
            # list_for_tuple.append(os.path.abspath(line))
            playlist_list.append(line.rstrip())

    if len(playlist_list) > 0:
        if not os.path.isfile('end_of_list.mp3'):
            engine.save_to_file(word_user_name + '''это последний трек в плейлисте.
                                Ты можешь запустить плейлист с начала.
                                Для этого обратись опять к другу''', 'test.mp3')
            engine.runAndWait()
            playlist_list.append('test.mp3')

    print('load_playlist(): Конец составления списка', time.time())
    print('load_playlist(): playlist_list', playlist_list)
    # playlist_list = list()

    return playlist_list

def play_vlc():
    # Если плеер уже запущен, но находится в состоянии пауза, то запускаем его (продолжаем играть)
    if media_list_player.get_state() == vlc.State(4):
        media_list_player.pause()
    else:
        # Если плеер еще не запущен - запускаем.
        # При этом создаем новый плейлист и загружаем в него список

        # Плейлист из файла загружаем в список (список, а не кортеж, т.к. планируется добавление в плейлист)
        # Пока загружается только плейлист из файла с названием my_playlist.m3u
        playlist_list = load_playlist('my_playlist.m3u')
        # playlist_list = load_playlist('my_playlist разные тесты.m3u')
        # playlist_list = load_playlist('8941.m3u')

        if len(playlist_list) == 0:
            say_text('play_vlc(): Плейлист пустой')
            return

        # vlc_instance = media_list_player.get_instance()
        media_list = vlc_instance.media_list_new()

        for song in playlist_list:
            media_list.add_media(song.rstrip())

        media_list_player.set_media_list(media_list)

        media_list_player.play()

        # time.sleep(0.1)


def say_text(text):
    engine.say(text)
    engine.runAndWait()


def commands_to_set(result_text):
    result_text = result_text.replace("\n", "")
    result_text = result_text.replace("partial", "")
    result_text = result_text.replace(":", "")
    result_text = result_text.replace("{", "")
    result_text = result_text.replace("}", "")
    result_text = result_text.replace('"', "")

    set_commands = set(result_text.split())

    return set_commands


def listen_to_user():
    record_seconds = 2
    listen = True
    max_replay = 1
    count_replay = 0
    max_len_rec = 100
    result_text = ''

    # stream.start_stream() Надо?
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

    print('listen_to_user(): result_tex: ', result_text.replace("\n", ""))

    return result_text


def look_for_short_command(set_commands):
    print('look_for_short_command(): set_commands: ', set_commands),
    set_play = {'играй', 'играть', 'пой', 'петь'}
    set_seek = {'найди', 'ищи', 'поиск', 'найти'}

    # Ищем и выполняем короткую команду

    # Если в словах пользователя не было ничего или было только слово друг
    if not set_commands:
        say_text(word_user_name + ', я не услышал команду. Обратись опять к другу')
        print('look_for_short_command(): я не услышал команду. Обратись опять к другу')
    elif not set_commands.isdisjoint(set_play):
        print('look_for_short_command(): Включаю плеер')
        say_text(word_user_name + ', включаю плеер')
        play_vlc()
    elif not set_commands.isdisjoint(set_seek):
        set_commands -= set_seek
        print('look_for_short_command(): Ищу')
        say_text(word_user_name + ', ищу ' + ' '.join(set_commands))
    else:
        # ни одна из коротких команд (играй, найди, назад, вперед, время и проч) не найдена =>
        # значит ждем когда пользователь опять обратится к другу
        say_text(word_user_name + ', я не смог распознать команду. Обратись опять к другу')
        print('look_for_short_command(): я не смог распознать команду. Обратись опять к другу')

def process_text_main(set_commands):
    set_commands -= {word_friend}
    print('process_text_main(): set_commands_user без слова друг:', set_commands)

    # Если кроме слова друг во множестве больше не было других слов (множество пустое),
    # значит надо запросить дальнейшие команды
    if not set_commands:
        say_text(word_user_name + word_hello)
        # Останавливаем поток, чтобы не попал шум (например речь друга) в речь пользователя
        stream.stop_stream()
        # и перезапускаем распознавание, чтобы убрать остатки былых слов
        rec.Reset()
        stream.start_stream()
        print('process_text_main(): set_commands пустое')
        print('process_text_main():  ', word_user_name, word_hello)
        result_text = listen_to_user()
        print('process_text_main(): result_text', result_text.replace("\n", ""))
        set_commands = commands_to_set(result_text)
        set_commands -= {word_friend}

    look_for_short_command(set_commands)


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

            print('main(): result_text :', result_text.replace("\n", ""), end='\n\n')

            print('main() before search friend: media_list_player.get_state(): ', media_list_player.get_state())
            print('main() before search friend: media_list_player.is_playing(): ', media_list_player.is_playing())

            if word_friend in result_text:
                set_commands = commands_to_set(result_text)
                if word_friend in set_commands:
                    # Как только услышали слово друг, останавливаем плеер, если он включен
                    if media_list_player.is_playing():
                        media_list_player.pause()

                    print('main(): обнаружено слово друг', ', set_commands=', set_commands, ', запускаем process_text_main')
                    process_text_main(set_commands)

            print('main() after search friend: media_list_player.get_state(): ', media_list_player.get_state())
            print('main(): after search friend media_list_player.is_playing(): ', media_list_player.is_playing())

            # vlc.State(6) может быть или если список закончился или если файл не воспроизводится (не медиа формат)
            if media_list_player.get_state() == vlc.State(6):
                media_player = media_list_player.get_media_player()

                # Если воспроизведение еще не началось, то это не медиа файл
                if media_player.get_position() == 0:
                    media_list_player.next()

                # Можно получить текущий воспроизводимый файл
                med = media_player.get_media()
                # med.tracks_get() если None, то значит это не медиа файл.
                # Можно использовать это условие, чтобы перейти к следующему треку,
                # но это еще один объект. Пока он не нужен
                # b1=med.tracks_get()
                # Смотрела также эти варианты
                # b3=med.get_mrl() можно получить имя трека
                # b2=med.get_tracks_info()
                # b5=med.get_state()
                # b6=med.get_type()

                print('main() (if media_list_player.get_state() == vlc.State(6)): ', media_list_player.get_state() == vlc.State(6))
                print('main(): med.get_mrl() = ', med.get_mrl())
                print('main(): med.get_state() = ', med.get_state())
                #
                # print('main(): media_list_player.get_state()', media_list_player.get_state())
                # print('main(): media_list_player.is_playing()',media_list_player.is_playing())

            # print('main() (if media_list_player.get_state() == vlc.State(6)): ',
            #       media_list_player.get_state() == vlc.State(6))
            # print('main(): med.get_mrl() = ', med.get_mrl())
            # print('main(): med.get_state() = ', med.get_state())

            print('main(): media_list_player.get_state()', media_list_player.get_state())
            print('main(): media_list_player.is_playing()', media_list_player.is_playing())

            rec.Reset()
            stream.stop_stream()
            stream.start_stream()
            print('main: rec.Reset(), stream.stop_stream(), stream.start_stream()')

    finally:
        stream.stop_stream()
        stream.close()
        py_audio.terminate()
        print('main: Программа закрыта')


if __name__ == '__main__':
    main()
