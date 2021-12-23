import os
from celery import Celery
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave

try:
    REDIS_BASE_URL = os.environ['REDIS_BASE_URL']
except KeyError:
    REDIS_BASE_URL = 'redis://localhost:6379'

celery = Celery(
    'asr-tasks',
    broker=f"{REDIS_BASE_URL}/0",
    backend=f"{REDIS_BASE_URL}/1",
    task_time_limit=30 * 60,
    task_soft_time_limit=30 * 60
)


class Config:
    enable_utc = True
    timezone = 'Europe/London'
    result_expires = 60 * 60 * 12  # 12 hours
    result_extended = True


celery.config_from_object(Config)

# set vosk log level
SetLogLevel(0)

# make sure to only load Model once
model = Model("model") if __name__ == '__main__' else None


@celery.task(name='asr', default_retry_delay=300, max_retry=5)
def recognize(data):
    try:
        file = wave.open(data['filename'], "rb")

        if (file.getnchannels() != 1 or
                file.getsampwidth() != 2 or
                file.getcomptype() != "NONE"
        ):
            return "Invalid wav file", 400
    except:
        return "Invalid audio file", 400

    rec = KaldiRecognizer(model, file.getframerate())
    rec.SetWords(True)
    rec.SetMaxAlternatives(0)

    while True:
        data = file.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    return rec.FinalResult()


if __name__ == '__main__':
    celery.start(argv=[
        'worker',
        # '--without-mingle',
        # '--without-gossip',
        # '--without-heartbeat'
        # '--loglevel=DEBUG',
        '--concurrency=2'
    ])
