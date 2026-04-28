import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = {}
        self.init_ui()
        self.reset_state()

    def reset_state(self):
        self.current = '0'

    def init_ui(self):
        self.setWindowTitle('iPhone Calculator')
        self.setFixedSize(320, 500)
        self.setStyleSheet("background-color: black;")

        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)

        # ⭐ 초기값 "0"으로 설정
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(100)

        self.display.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: white;
                border: none;
                font-size: 40px;
                padding-right: 10px;
            }
        """)

        grid.addWidget(self.display, 0, 0, 1, 4)

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

        for row_idx, row in enumerate(buttons):
            col = 0
            for btn in row:
                button = QPushButton(btn)
                button.clicked.connect(self.on_click)

                self.buttons[btn] = button
                self.set_button_style(button, btn)

                if btn == '0':
                    button.setFixedSize(140, 60)
                    grid.addWidget(button, row_idx + 1, col, 1, 2)
                    col += 2
                else:
                    button.setFixedSize(60, 60)
                    grid.addWidget(button, row_idx + 1, col)
                    col += 1

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

    # ⭐ 폰트 자동 조절
    def adjust_font_size(self, text):
        length = len(text)

        if length <= 6:
            size = 40
        elif length <= 10:
            size = 30
        elif length <= 15:
            size = 24
        else:
            size = 18

        self.display.setStyleSheet(f"""
            QLineEdit {{
                background-color: black;
                color: white;
                border: none;
                font-size: {size}px;
                padding-right: 10px;
            }}
        """)

    # ⭐ 소수점 처리 (입력 중 보호 포함)
    def format_number(self, value):
        try:
            # 연산 중이면 건드리지 않음
            if ' ' in value:
                return value

            # ⭐ 소수점 입력 중이면 유지 (핵심!!)
            if value.endswith('.'):
                return value

            num = float(value)

            # 정수면 .0 제거
            if num.is_integer():
                return str(int(num))

            return str(round(num, 6))
        except:
            return value

    #calculate 함수
    def calculate(self, expression):
        tokens = expression.split()

        if len(tokens) != 3:
            return "Error"

        a, op, b = tokens

        try:
            a, b = float(a), float(b)
        except:
            return "Error"

        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '×':
            return a * b
        elif op == '÷':
            if b == 0:
                return "Error"
            return a / b

    def on_click(self):
        text = self.sender().text()
        current = self.display.text()

        try:
            # 숫자 입력
            if text.isdigit():
                if current == "0":
                    self.display.setText(text)
                else:
                    self.display.setText(current + text)

            # 소수점
            elif text == '.':
                if '.' not in current:
                    if current == "0":
                        self.display.setText("0.")
                    else:
                        self.display.setText(current + '.')

            # 초기화
            elif text == 'AC':
                self.display.setText("0")
                self.reset_state()

            # 부호 변경
            elif text == '+/-':
                if current.startswith('-'):
                    self.display.setText(current[1:])
                else:
                    self.display.setText('-' + current)

            # 퍼센트
            elif text == '%':
                val = float(current)
                self.display.setText(str(val / 100))

            # 연산자
            elif text in ['+', '-', '×', '÷']:
                self.display.setText(current + ' ' + text + ' ')

            # 결과
            elif text == '=':
                result = self.calculate(current)
                self.display.setText(str(result))

            # 보너스 과제
            formatted = self.format_number(self.display.text())
            self.display.setText(formatted)
            self.adjust_font_size(formatted)

        except:
            self.display.setText("Error")
            self.reset_state()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())