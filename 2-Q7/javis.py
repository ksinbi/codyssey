import os
from datetime import datetime

import sounddevice as sd
from scipy.io.wavfile import write


class VoiceRecorder:
    def __init__(self):
        self.sample_rate = 44100

    def create_records_folder(self):
        if not os.path.exists('records'):
            os.makedirs('records')

    def create_file_name(self):
        now = datetime.now()

        return now.strftime('%Y%m%d-%H%M%S.wav')
    
    def record_voice(self, seconds = 5):
        self.create_records_folder()

        file_name = self.create_file_name()
        file_path = os.path.join('records', file_name)

        print('녹음을 시작합니다.')

        recording = sd.rec(
            int(seconds * self.sample_rate),
            samplerate = self.sample_rate,
            channels = 1,
            dtype = 'int16'
        )

        sd.wait()

        print('녹음이 완료되었습니다.')

        write(file_path, self.sample_rate, recording)

        print(f'저장 위치: {file_path}')


def main():
    recorder = VoiceRecorder()

    try:
        seconds = int(input('녹음 시간을 입력하세요(초): '))

        recorder.record_voice(seconds)

    except ValueError:
        print('숫자를 입력해야 합니다.')


if __name__ == '__main__':
    main()