import json
import platform
import os
import subprocess
import time


class MissionComputer:
    """미션 컴퓨터의 시스템 정보와 부하를 관리하는 클래스."""

    def __init__(self, setting_file='setting.txt'):
        """설정 파일을 불러온다."""
        self.settings = self._load_settings(setting_file)

    def _load_settings(self, setting_file):
        """setting.txt 파일에서 출력 항목을 불러온다."""
        default_settings = {
            'operating_system': True,
            'os_version': True,
            'cpu_type': True,
            'cpu_cores': True,
            'memory_size_gb': True,
            'cpu_usage_percent': True,
            'memory_usage_percent': True
        }

        if not os.path.exists(setting_file):
            return default_settings

        try:
            with open(setting_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        default_settings[key.strip()] = (
                            value.strip().lower() == 'true'
                        )
        except Exception as error:
            print(f"설정 파일을 읽는 중 오류 발생: {error}")

        return default_settings

    def get_mission_computer_info(self):
        """시스템 정보를 반환한다."""
        info = {}

        try:
            if self.settings.get('operating_system'):
                info['operating_system'] = platform.system()

            if self.settings.get('os_version'):
                info['os_version'] = platform.version()

            if self.settings.get('cpu_type'):
                cpu = platform.processor() or platform.machine()
                info['cpu_type'] = cpu

            if self.settings.get('cpu_cores'):
                info['cpu_cores'] = os.cpu_count()

            if self.settings.get('memory_size_gb'):
                info['memory_size_gb'] = self._get_total_memory()

        except Exception as error:
            info['error'] = str(error)

        return info

    def get_mission_computer_load(self):
        """시스템 부하 정보를 반환한다."""
        load = {}

        try:
            if self.settings.get('cpu_usage_percent'):
                load['cpu_usage_percent'] = self._get_cpu_usage()

            if self.settings.get('memory_usage_percent'):
                load['memory_usage_percent'] = self._get_memory_usage()

        except Exception as error:
            load['error'] = str(error)

        return load

    def _run_command(self, command):
        """시스템 명령어 실행."""
        return subprocess.check_output(
            command, stderr=subprocess.DEVNULL, text=True
        ).strip()

    def _get_total_memory(self):
        """총 메모리 크기를 GB 단위로 반환한다."""
        try:
            system = platform.system()

            if system == 'Windows':
                output = self._run_command([
                    'wmic', 'computersystem', 'get',
                    'TotalPhysicalMemory'
                ])
                for line in output.splitlines():
                    if line.strip().isdigit():
                        memory_bytes = int(line.strip())
                        return round(memory_bytes / (1024 ** 3), 2)

            elif system == 'Darwin':  # macOS
                memory_bytes = int(
                    self._run_command(['sysctl', '-n', 'hw.memsize'])
                )
                return round(memory_bytes / (1024 ** 3), 2)

            elif system == 'Linux':
                with open('/proc/meminfo', 'r', encoding='utf-8') as file:
                    for line in file:
                        if line.startswith('MemTotal'):
                            memory_kb = int(line.split()[1])
                            return round(memory_kb / (1024 ** 2), 2)

        except Exception:
            return 'Unavailable'

        return 'Unavailable'

    def _get_memory_usage(self):
        """메모리 사용률을 퍼센트로 반환한다."""
        try:
            system = platform.system()

            if system == 'Windows':
                output = self._run_command([
                    'wmic', 'OS', 'get',
                    'FreePhysicalMemory,TotalVisibleMemorySize', '/Value'
                ])
                values = {}
                for line in output.splitlines():
                    if '=' in line:
                        key, value = line.split('=')
                        values[key.strip()] = int(value.strip())

                total = values.get('TotalVisibleMemorySize', 0)
                free = values.get('FreePhysicalMemory', 0)

                if total > 0:
                    used = total - free
                    return round((used / total) * 100, 2)

            elif system == 'Darwin':  # macOS
                total_bytes = int(
                    self._run_command(['sysctl', '-n', 'hw.memsize'])
                )

                vm_output = self._run_command(['vm_stat'])
                pages = {}

                for line in vm_output.splitlines():
                    if ':' in line:
                        key, value = line.split(':')
                        pages[key.strip()] = int(
                            value.strip().replace('.', '')
                        )

                page_size = 4096
                free_pages = (
                    pages.get('Pages free', 0) +
                    pages.get('Pages inactive', 0) +
                    pages.get('Pages speculative', 0)
                )

                free_bytes = free_pages * page_size
                used_bytes = total_bytes - free_bytes

                if total_bytes > 0:
                    return round((used_bytes / total_bytes) * 100, 2)

            elif system == 'Linux':
                mem_info = {}
                with open('/proc/meminfo', 'r', encoding='utf-8') as file:
                    for line in file:
                        key, value = line.split(':')
                        mem_info[key] = int(value.strip().split()[0])

                total = mem_info.get('MemTotal', 0)
                available = mem_info.get('MemAvailable', 0)

                if total > 0:
                    used = total - available
                    return round((used / total) * 100, 2)

        except Exception:
            return 'Unavailable'

        return 'Unavailable'

    def _get_cpu_usage(self):
        """CPU 사용률을 퍼센트로 반환한다."""
        try:
            system = platform.system()

            if system == 'Windows':
                output = self._run_command(
                    ['wmic', 'cpu', 'get', 'loadpercentage']
                )
                for line in output.splitlines():
                    line = line.strip()
                    if line.isdigit():
                        return float(line)

            elif system == 'Darwin':  # macOS
                output = self._run_command(
                    ['top', '-l', '1', '-n', '0']
                )
                for line in output.splitlines():
                    if 'CPU usage' in line:
                        parts = line.split(',')
                        for part in parts:
                            if 'idle' in part:
                                idle = float(
                                    part.strip().split()[0].replace('%', '')
                                )
                                return round(100 - idle, 2)

            elif system == 'Linux':
                with open('/proc/stat', 'r', encoding='utf-8') as file:
                    first = file.readline().split()

                idle1 = int(first[4])
                total1 = sum(map(int, first[1:]))

                time.sleep(1)

                with open('/proc/stat', 'r', encoding='utf-8') as file:
                    second = file.readline().split()

                idle2 = int(second[4])
                total2 = sum(map(int, second[1:]))

                idle_delta = idle2 - idle1
                total_delta = total2 - total1

                if total_delta > 0:
                    usage = 100 * (1 - idle_delta / total_delta)
                    return round(usage, 2)

        except Exception:
            return 'Unavailable'

        return 'Unavailable'

    @staticmethod
    def print_json(data):
        """데이터를 JSON 형식으로 출력한다."""
        print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    run_computer = MissionComputer()

    print('\n=== Mission Computer System Information ===')
    run_computer.print_json(run_computer.get_mission_computer_info())

    print('\n=== Mission Computer Load Information ===')
    run_computer.print_json(run_computer.get_mission_computer_load())