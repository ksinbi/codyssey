import os


def analyze_mission_log(log_filename):
    try:
        #파일 존재 확인
        if not os.path.exists(log_filename):
            print(f"오류: {log_filename} 파일을 찾을 수 없습니다.")
            return

        #로그 읽기
        with open(log_filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        #전체 로그 출력
        print('--- 전체 로그 내용 ---')
        for line in lines:
            print(line.strip())

        #문제 키워드 정의
        issue_keywords = ['ERROR', 'CRITICAL', 'unstable', 'explosion']

        #문제 로그 추출
        issue_logs = [
            line.strip()
            for line in lines
            if any(keyword in line for keyword in issue_keywords)
        ]

        # 시간 역순 로그
        reversed_logs = lines[::-1]

        #문제 로그 파일 따로 저장
        with open('issue_logs.txt', 'w', encoding='utf-8') as issue_file:
            if issue_logs:
                for issue in issue_logs:
                    issue_file.write(issue + '\n')
            else:
                issue_file.write('특이 사항 없음\n')

        #Markdown 보고서 생성
        with open('log_analysis.md', 'w', encoding='utf-8') as report:
            report.write('# 화성 기지 사고 원인 분석 보고서\n\n')
            report.write(f'## 1. 분석 대상 파일\n{log_filename}\n\n')
            report.write(f'## 2. 총 로그 수\n{len(lines)}개\n\n')

            report.write('## 3. 발견된 문제 로그\n')
            if issue_logs:
                for issue in issue_logs:
                    report.write(f'- {issue}\n')
            else:
                report.write('- 특이 사항 없음\n')

            report.write('\n## 4. 전체 로그 (시간 역순)\n')
            report.write('```\n')
            for log in reversed_logs:
                report.write(log)
            report.write('```\n')

        print("\n분석 완료:")
        print(" - log_analysis.md 생성 완료")
        print(" - issue_logs.txt 생성 완료")

    except Exception as e:
        print(f'예상치 못한 오류가 발생했습니다: {e}')


if __name__ == '__main__':
    print('Hello Mars')
    analyze_mission_log('mission_computer_main.log')
