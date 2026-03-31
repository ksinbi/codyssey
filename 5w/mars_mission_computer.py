import random
from datetime import datetime


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
        self._save_log()
        return self.env_values

    def _save_log(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        log_line = (
            f'{now}, '
            f'{self.env_values["mars_base_internal_temperature"]}°C, '
            f'{self.env_values["mars_base_external_temperature"]}°C, '
            f'{self.env_values["mars_base_internal_humidity"]}%, '
            f'{self.env_values["mars_base_external_illuminance"]}W/m2, '
            f'{self.env_values["mars_base_internal_co2"]}%, '
            f'{self.env_values["mars_base_internal_oxygen"]}%\n'
        )

        with open('env_log.txt', 'a', encoding='utf-8') as file:
            file.write(log_line)


if __name__ == '__main__':
    ds = DummySensor()

    ds.set_env()
    env = ds.get_env()

    print('=' * 50)
    print('      Mars Base Environment Status')
    print('=' * 50)

    print(f'내부 온도        : {env["mars_base_internal_temperature"]:>6} °C')
    print(f'외부 온도        : {env["mars_base_external_temperature"]:>6} °C')
    print(f'내부 습도        : {env["mars_base_internal_humidity"]:>6} %')
    print(f'외부 광량        : {env["mars_base_external_illuminance"]:>6} W/m2')
    print(f'내부 CO2 농도    : {env["mars_base_internal_co2"]:>6} %')
    print(f'내부 산소 농도   : {env["mars_base_internal_oxygen"]:>6} %')

    print('=' * 50)