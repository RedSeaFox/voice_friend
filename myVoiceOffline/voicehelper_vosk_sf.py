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
# RECORD_SECONDS = 2

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
    """ Обработка указаний пользователя"""

    # Сначала сообщаем пользователю, что друг услышал, что пользователь позвал друга.
    say_text(word_user_name + word_hello)
    stream.stop_stream()
    print(word_user_name + word_hello)

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

        print(count_replay, len(rec.PartialResult()),len(result_text), result_text)

    # Обрабатываем команду
    if 'играй' in result_text:
        print(word_user_name + ', включаю плеер')
        say_text(word_user_name + ', включаю плеер')

def main():
    # Ждем обращение пользователя к другу, т.е. ждем, когда пользователь скажет слово друг,
    # для этого достаточно 2 секунд.
    # 1 секунды мало, так как в этом случае возможно частое попадание слова друг на границу секунды
    # 3 секунды много, так как получаются значительные паузы в реакции друга
    record_seconds = 2

    say_text('Программа запущена')

    # Слушаем постоянно
    try:
        listen = True
        while listen:
            # Обрабатываем порцию за record_seconds секунд
            for _ in range(0, RATE // CHUNK * record_seconds):
                data = stream.read(CHUNK)
                rec.AcceptWaveform(data)

            result_text = rec.PartialResult()
            # print(result_text)
            # Если услышали, что пользователь обращается к другу, то вызываем обработчик, который
            # будет выполнять дальнейшие действия (спрашивать пользователя, запускать другие обработчики)
            if word_friend in result_text:
                rec.Reset()
                stream.stop_stream()
                working_with_commands()
                stream.start_stream()
                # rec.Reset()

            # В противном случае считаем, что пользователь не обращался к другу.
            # Чтобы не копить распознанный текст, очищаем rec
            # else:
                # rec.Reset()

    finally:
        print('Closing programm Ok')
        py_audio.terminate()

if __name__ == '__main__':
    main()

