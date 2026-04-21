import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = {}  # 버튼 저장
        self.init_ui() # UI 초기화 함수 호출

    def init_ui(self):
        self.setWindowTitle('iPhone Calculator')
        self.setFixedSize(320, 500)
        self.setStyleSheet("background-color: black;")  # 배경색 검정

        # 그리드 레이아웃 생성 (버튼 배치용)
        grid = QGridLayout()
        grid.setSpacing(10)  # 버튼 간격
        self.setLayout(grid)

        # 디스플레이
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        self.display.setReadOnly(True)  # 직접 입력 못하게 막기
        self.display.setFixedHeight(100)
        
        # 스타일 적용
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: white;
                border: none;
                font-size: 40px;
                padding-right: 10px;
            }
        """)
        # 그리드 0행에 디스플레이 추가 (4칸 차지)
        grid.addWidget(self.display, 0, 0, 1, 4)

        # 버튼 색상 딕셔너리
        self.button_styles = {
            'AC':  "#a5a5a5", '+/-': "#a5a5a5", '%': "#a5a5a5",
            '÷': "#ff9f0a", '×': "#ff9f0a", '-': "#ff9f0a", '+': "#ff9f0a", '=': "#ff9f0a",

            '0': "#333333", '1': "#333333", '2': "#333333",
            '3': "#333333", '4': "#333333", '5': "#333333",
            '6': "#333333", '7': "#333333", '8': "#333333",
            '9': "#333333", '.': "#333333",
        }

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # 버튼 생성
        for row_idx, row in enumerate(buttons):
            col = 0
            for btn in row:
                button = QPushButton(btn)
                button.clicked.connect(self.on_click)# 클릭 시 함수 연결

                self.buttons[btn] = button  # 저장

                # 색상 적용
                self.set_button_style(button, btn)

                # 크기 및 배치
                if btn == '0':
                    button.setFixedSize(140, 60)
                    grid.addWidget(button, row_idx + 1, col, 1, 2)
                    col += 2
                else:
                    button.setFixedSize(60, 60)
                    grid.addWidget(button, row_idx + 1, col)
                    col += 1

    # 버튼 스타일 함수
    def set_button_style(self, button, btn):
        color = self.button_styles.get(btn, "#333333")
        text_color = "black" if color == "#a5a5a5" else "white"

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: {text_color};
                border-radius: 30px;
                font-size: 20px;
            }}
            QPushButton:pressed {{
                background-color: #888888;
            }}
        """)

    def on_click(self):
        sender = self.sender()  # 클릭된 버튼 가져오기
        text = sender.text()    # 버튼의 텍스트
        current = self.display.text()  # 현재 디스플레이 값

        # 숫자 입력 및 소수점 입력
        if text.isdigit() or text == '.':
            self.display.setText(current + text)

        # 전체 초기화
        elif text == 'AC':
            self.display.clear()
            
        # 부호 변경
        elif text == '+/-':
            if current:
                if current.startswith('-'):
                    self.display.setText(current[1:])
                else:
                    self.display.setText('-' + current)

        elif text == '%':
            try:
                value = float(current)
                self.display.setText(str(value / 100))
            except:
                self.display.setText("Error")

        elif text in ['+', '-', '×', '÷']:
            self.display.setText(current + ' ' + text + ' ')
            
        # 결과 계산 (=)
        elif text == '=':
            try:
                expression = current.replace('×', '*').replace('÷', '/')
                
                result = eval(expression)
                self.display.setText(str(result))
            except:
                self.display.setText("Error")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())