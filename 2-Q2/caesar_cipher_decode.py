# caesar_cipher_decode.py
import string


def caesar_cipher_decode(target_text):
    """
    카이사르 암호를 해독하는 함수

    :param target_text: 해독할 문자열
    :return: 해독 결과 리스트
    """
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    result_list = []

    # 알파벳 개수(26)만큼 반복
    for shift in range(len(lowercase)):
        decoded_text = ''

        for char in target_text:
            # 소문자 처리
            if char in lowercase:
                index = lowercase.index(char)
                new_index = (index - shift) % len(lowercase)
                decoded_text += lowercase[new_index]

            # 대문자 처리
            elif char in uppercase:
                index = uppercase.index(char)
                new_index = (index - shift) % len(uppercase)
                decoded_text += uppercase[new_index]

            # 알파벳이 아니면 그대로 유지
            else:
                decoded_text += char

        result_list.append(decoded_text)

        print('-' * 60)
        print(f'자리수: {shift}')
        print(f'해독 결과: {decoded_text}')

    return result_list


def save_result(result_text):
    """
    result.txt 파일로 저장하는 함수

    :param result_text: 저장할 문자열
    """
    try:
        with open('result.txt', 'w', encoding='utf-8') as file:
            file.write(result_text)

        print('\n[+] result.txt 파일 저장 완료')

    except FileNotFoundError:
        print('[!] 파일 경로를 찾을 수 없습니다.')

    except PermissionError:
        print('[!] 파일 접근 권한이 없습니다.')

    except OSError:
        print('[!] 파일 저장 중 오류가 발생했습니다.')


# 프로그램 시작
if __name__ == '__main__':
    try:
        # password.txt 읽기
        with open('password.txt', 'r', encoding='utf-8') as file:
            encrypted_text = file.read().strip()

        print('=' * 60)
        print('[*] password.txt 읽기 성공')
        print(f'[*] 암호문: {encrypted_text}')
        print('=' * 60)

        # 카이사르 암호 해독
        decoded_results = caesar_cipher_decode(encrypted_text)

        print('\n' + '=' * 60)
        print('[*] 위 결과를 확인한 뒤 올바른 자리수를 입력하세요.')

        # 사용자 입력
        while True:
            try:
                correct_shift = int(input('정답 자리수 입력: '))

                if 0 <= correct_shift < 26:
                    break

                print('[!] 0 ~ 25 사이 숫자를 입력하세요.')

            except ValueError:
                print('[!] 숫자만 입력하세요.')

        final_result = decoded_results[correct_shift]

        print('\n' + '=' * 60)
        print(f'[+] 최종 해독 결과: {final_result}')
        print('=' * 60)

        # 결과 저장
        save_result(final_result)

    except FileNotFoundError:
        print('[!] password.txt 파일이 존재하지 않습니다.')

    except PermissionError:
        print('[!] password.txt 파일 접근 권한이 없습니다.')

    except OSError:
        print('[!] 파일 처리 중 오류가 발생했습니다.')
