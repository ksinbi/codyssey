import zipfile
import itertools
import string
import time
import zlib
import sys

def unlock_zip():
    zip_filename = 'emergency_storage_key.zip'
    
    # 설정: 소문자 + 숫자 (6자리)
    chars = string.ascii_lowercase + string.digits
    start_time = time.time()
    attempt = 0

    print(f"[*] 대상 파일: {zip_filename}")
    print(f"[*] 해독 시작 시간: {time.ctime(start_time)}")
    print("-" * 50)

    try:
        with zipfile.ZipFile(zip_filename) as zf:
            # 6자리 모든 조합 생성
            for combo in itertools.product(chars, repeat=6):
                password = ''.join(combo)
                attempt += 1

                try:
                    # 압축 해제 시도
                    zf.extractall(pwd=password.encode('utf-8'))
                    
                    # [성공] 비밀번호를 찾았을 때
                    end_time = time.time()
                    total_elapsed = end_time - start_time
                    
                    print(f"\n\n" + "="*50)
                    print(f"[+] 성공! 비밀번호 발견: {password}")
                    print(f"[+] 총 시도 횟수: {attempt:,}번")
                    print(f"[+] 총 소요 시간: {total_elapsed:.2f}초")
                    print(f"[+] 종료 시각: {time.ctime(end_time)}")
                    print("="*50)
                    
                    with open('password_found.txt', 'w') as f:
                        f.write(password)
                    return True

                except (RuntimeError, zlib.error, zipfile.BadZipFile):
                    # 암호가 틀려 발생하는 에러들을 무시하고 다음 조합으로 진행
                    if attempt % 1000 == 0:
                        elapsed = time.time() - start_time
                        speed = attempt / elapsed if elapsed > 0 else 0
                        # \r을 이용해 한 줄에서 실시간 업데이트
                        sys.stdout.write(f"\r[>] 진행 중... {attempt:,} 시도 ({speed:.0f} p/s) | 현재: {password}  ")
                        sys.stdout.flush()
                    continue

    except FileNotFoundError:
        print(f"\n[!] 에러: '{zip_filename}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"\n[!] 기타 에러 발생: {e}")

    # [실패] 모든 조합을 시도했으나 못 찾았을 때
    end_time = time.time()
    total_elapsed = end_time - start_time
    print(f"\n\n" + "-"*50)
    print(f"[-] 해독 실패: 6자리 조합 내에 비밀번호가 없습니다.")
    print(f"[-] 총 시도 횟수: {attempt:,}번")
    print(f"[-] 총 소요 시간: {total_elapsed:.2f}초")
    print(f"[-] 종료 시각: {time.ctime(end_time)}")
    print("-" * 50)
    
    return False

if __name__ == '__main__':
    unlock_zip()