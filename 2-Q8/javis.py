import os
import whisper
import pandas as pd
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write

class VoiceRecorder:
    def __init__(self):
        self.sample_rate = 44100
        # 모델은 "base"를 사용합니다 (속도와 정확도의 균형). 
        # 성능을 높이려면 "small"이나 "medium"으로 변경하세요.
        self.model = whisper.load_model("base")

    def create_records_folder(self):
        if not os.path.exists('records'):
            os.makedirs('records')

    def create_file_name(self):
        now = datetime.now()
        return now.strftime('%Y%m%d-%H%M%S.wav')

    def record_voice(self, seconds=5):
        self.create_records_folder()
        file_name = self.create_file_name()
        file_path = os.path.join('records', file_name)

        print('\n녹음을 시작합니다...')
        recording = sd.rec(
            int(seconds * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()
        print('녹음이 완료되었습니다.')
        
        write(file_path, self.sample_rate, recording)
        print(f'저장 위치: {file_path}')
        
        # 녹음 직후 STT 변환 여부 확인 (선택 사항)
        return file_path

    def transcribe_voice(self, file_path):
        """
        음성 파일에서 텍스트를 추출하고 CSV로 저장한다.
        """
        if not os.path.exists(file_path):
            print(f"파일을 찾을 수 없습니다: {file_path}")
            return

        print(f"\n'{os.path.basename(file_path)}' 텍스트 변환 중... 잠시만 기다려주세요.")
        
        # STT 실행
        result = self.model.transcribe(file_path, fp16=False)
        
        # 데이터 구조화 (시작 시간, 종료 시간, 텍스트)
        segments = result['segments']
        data = []
        for segment in segments:
            data.append({
                'start_time': f"{segment['start']:.2f}s",
                'end_time': f"{segment['end']:.2f}s",
                'text': segment['text'].strip()
            })

        # DataFrame 생성 및 CSV 저장
        df = pd.DataFrame(data)
        csv_name = os.path.splitext(file_path)[0] + '.csv'
        df.to_csv(csv_name, index=False, encoding='utf-8-sig')
        
        print(f"텍스트 추출 완료! CSV 저장 위치: {csv_name}")
        print("-" * 30)
        for d in data:
            print(f"[{d['start_time']} -> {d['end_time']}] {d['text']}")

    def show_files_by_date_range(self):
        if not os.path.exists('records'):
            print('\nrecords 폴더가 존재하지 않습니다.')
            return []

        start_date = input('\n시작 날짜 입력 (예: 20260501): ')
        end_date = input('종료 날짜 입력 (예: 20260531): ')

        file_list = os.listdir('records')
        matched_files = [f for f in file_list if f.endswith('.wav') and start_date <= f[:8] <= end_date]
        matched_files.sort()

        if not matched_files:
            print('해당 날짜 범위의 파일이 없습니다.')
            return []

        print('\n===== 조회 결과 =====')
        for idx, file_name in enumerate(matched_files):
            print(f"{idx + 1}. {file_name}")
        
        return matched_files

def show_menu():
    print('\n===== 음성 녹음 및 STT 프로그램 =====')
    print('1. 음성 녹음')
    print('2. 날짜 범위 파일 조회 및 STT 변환')
    print('3. 프로그램 종료')

def main():
    recorder = VoiceRecorder()

    while True:
        show_menu()
        choice = input('\n원하는 기능을 선택하세요: ')

        if choice == '1':
            try:
                seconds = int(input('녹음 시간을 입력하세요(초): '))
                file_path = recorder.record_voice(seconds)
                
                # 녹음 후 바로 변환할지 선택
                run_stt = input("방금 녹음한 파일을 바로 텍스트로 변환할까요? (y/n): ")
                if run_stt.lower() == 'y':
                    recorder.transcribe_voice(file_path)
            except ValueError:
                print('숫자를 입력해야 합니다.')

        elif choice == '2':
            matched_files = recorder.show_files_by_date_range()
            if matched_files:
                sub_choice = input('\nSTT 변환할 파일 번호를 입력하세요 (취소는 0): ')
                if sub_choice.isdigit() and 0 < int(sub_choice) <= len(matched_files):
                    target_file = matched_files[int(sub_choice) - 1]
                    recorder.transcribe_voice(os.path.join('records', target_file))

        elif choice == '3':
            print('\n프로그램을 종료합니다.')
            break
        else:
            print('\n올바른 메뉴 번호를 입력하세요.')

if __name__ == '__main__':
    main()