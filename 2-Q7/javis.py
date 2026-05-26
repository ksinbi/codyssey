import os
from datetime import datetime

import sounddevice as sd
from scipy.io.wavfile import write


class VoiceRecorder:
    def __init__(self):
        self.sample_rate = 44100

    def create_records_folder(self):
        """
        records 폴더가 없으면 생성한다.
        """
        if not os.path.exists('records'):
            os.makedirs('records')

    def create_file_name(self):
        """
        현재 날짜와 시간을 기반으로 파일 이름을 생성한다.
        """
        now = datetime.now()

        return now.strftime('%Y%m%d-%H%M%S.wav')

    def record_voice(self, seconds = 5):
        """
        음성을 녹음하고 wav 파일로 저장한다.
        """
        self.create_records_folder()

        file_name = self.create_file_name()
        file_path = os.path.join('records', file_name)

        print('\n녹음을 시작합니다.')

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

    def show_files_by_date_range(self):
        """
        특정 날짜 범위의 녹음 파일을 출력한다.
        """
        if not os.path.exists('records'):
            print('\nrecords 폴더가 존재하지 않습니다.')
            return

        start_date = input('\n시작 날짜 입력 (예: 20260501): ')
        end_date = input('종료 날짜 입력 (예: 20260531): ')

        file_list = os.listdir('records')

        matched_files = []

        for file_name in file_list:
            if not file_name.endswith('.wav'):
                continue

            file_date = file_name[:8]

            if start_date <= file_date <= end_date:
                matched_files.append(file_name)

        matched_files.sort()

        print('\n===== 조회 결과 =====')

        if len(matched_files) == 0:
            print('해당 날짜 범위의 파일이 없습니다.')
            return

        for file_name in matched_files:
            print(file_name)


def show_menu():
    """
    메뉴를 출력한다.
    """
    print('\n===== 음성 녹음 프로그램 =====')
    print('1. 음성 녹음')
    print('2. 날짜 범위 파일 조회')
    print('3. 프로그램 종료')


def main():
    recorder = VoiceRecorder()

    while True:
        show_menu()

        choice = input('\n원하는 기능을 선택하세요: ')

        if choice == '1':
            try:
                seconds = int(input('녹음 시간을 입력하세요(초): '))

                recorder.record_voice(seconds)

            except ValueError:
                print('숫자를 입력해야 합니다.')

        elif choice == '2':
            recorder.show_files_by_date_range()

        elif choice == '3':
            print('\n프로그램을 종료합니다.')
            break

        else:
            print('\n올바른 메뉴 번호를 입력하세요.')


if __name__ == '__main__':
    main()