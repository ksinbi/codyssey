import zipfile
import itertools
import string
import time
import zlib
import sys

def unlock_zip():
    zip_filename = 'emergency_storage_key.zip'
    chars = string.ascii_lowercase + string.digits
    start_time = time.time()
    attempt = 0
    
    # 6자리 전체 조합 수 (약 21억 개)
    total_combinations = len(chars) ** 6

    print(f"[*] Target: {zip_filename}")
    print(f"[*] Total combinations: {total_combinations:,}")
    print("-" * 50)

    try:
        with zipfile.ZipFile(zip_filename) as zf:
            for combo in itertools.product(chars, repeat=6):
                password = ''.join(combo)
                attempt += 1

                try:
                    zf.extractall(pwd=password.encode('utf-8'))
                    
                    # 성공 시 출력
                    elapsed = time.time() - start_time
                    print(f"\n\n[+] SUCCESS!")
                    print(f"[+] Password: {password}")
                    print(f"[+] Time: {elapsed:.2f}s | Attempts: {attempt:,}")
                    return True

                except (RuntimeError, zlib.error, zipfile.BadZipFile):
                    # 1000번마다 터미널 업데이트
                    if attempt % 1000 == 0:
                        elapsed = time.time() - start_time
                        speed = attempt / elapsed if elapsed > 0 else 0
                        # :<20 등을 사용해 고정 너비를 확보하여 숫자가 밀리지 않게 함
                        sys.stdout.write(f"\r[>] {attempt:,} attempts ({speed:.0f} p/s) | Current: {password}  ")
                        sys.stdout.flush()
                    continue

    except FileNotFoundError:
        print(f"\n[!] Error: File not found.")
    
    print("\n[-] Failed to find password.")
    return False

if __name__ == '__main__':
    unlock_zip()