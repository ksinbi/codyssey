import time
import json
import random
import threading


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        self.set_env()
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values = {}
        self.ds = DummySensor()
        self.running = True
        self.history = []

        # 한국어 키 매핑
        self.key_map = {
            'mars_base_internal_temperature': '내부 온도 (°C)',
            'mars_base_external_temperature': '외부 온도 (°C)',
            'mars_base_internal_humidity': '내부 습도 (%)',
            'mars_base_external_illuminance': '외부 광량 (lx)',
            'mars_base_internal_co2': '이산화탄소 농도 (ppm)',
            'mars_base_internal_oxygen': '산소 농도 (%)'
        }

    def stop_system(self):
        while self.running:
            user_input = input()

            if user_input.strip().lower() in ['stop', 'exit', 'quit']:
                self.running = False
                print('System stoped...')
                break

    def print_average(self):
        if not self.history:
            return

        avg = {}
        keys = self.history[0].keys()

        for key in keys:
            avg[key] = round(
                sum(item[key] for item in self.history) / len(self.history), 2
            )

        # 한국어 키 변환
        formatted_avg = {}
        for key, value in avg.items():
            kor_key = self.key_map.get(key, key)
            formatted_avg[kor_key] = value

        print('\n===== 5분 평균 값 =====')
        print(json.dumps(formatted_avg, indent=4, ensure_ascii=False))
        print('=====================\n')

    def get_sensor_data(self):
        # 입력 감지용 스레드
        thread = threading.Thread(target=self.stop_system)
        thread.daemon = True
        thread.start()

        start_time = time.time()

        while self.running:
            # 센서 값 가져오기
            data = self.ds.get_env()

            # 안전하게 복사
            self.env_values = data.copy()
            self.history.append(data.copy())

            # 한국어 JSON 변환
            formatted_data = {}
            for key, value in self.env_values.items():
                kor_key = self.key_map.get(key, key)
                formatted_data[kor_key] = value

            # JSON 출력
            print('\n===== 화성 기지 환경 정보 =====')
            print(json.dumps(formatted_data, indent=4, ensure_ascii=False))
            print('=============================\n')

            # 5분(300초)마다 평균 출력
            if time.time() - start_time >= 300:
                self.print_average()
                self.history = []
                start_time = time.time()

            time.sleep(5)


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()