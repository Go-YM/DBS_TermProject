import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QHBoxLayout, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('DBS: Term Project')

        banner_label = QLabel(self)
        banner_label.setGeometry(0, 0, self.width(), 50)
        banner_label.setStyleSheet("background-color: #4CAF50; color: white;")
        banner_label.setAlignment(Qt.AlignCenter)
        banner_label.setFont(QFont('Arial', 20))
        banner_label.setText("중고차 매매 시스템")

        self.id_label = QLabel('ID:', self)
        self.id_label.setGeometry(230, 200, 50, 30)

        self.id_input = QLineEdit(self)
        self.id_input.setGeometry(300, 200, 200, 30)

        self.pw_label = QLabel('PW:', self)
        self.pw_label.setGeometry(230, 250, 50, 30)

        self.pw_input = QLineEdit(self)
        self.pw_input.setGeometry(300, 250, 200, 30)
        self.pw_input.setEchoMode(QLineEdit.Password)  

        login_button = QPushButton('로그인', self)
        login_button.setGeometry(300, 300, 100, 30)
        login_button.clicked.connect(self.login_button_clicked)

        signup_button = QPushButton('회원가입', self)
        signup_button.setGeometry(400, 300, 100, 30)
        signup_button.clicked.connect(self.show_registration_window)

        self.show()

    def login_button_clicked(self):
        id_text = self.id_input.text()
        pw_text = self.pw_input.text()

        if id_text == '123' and pw_text == '123':
            QMessageBox.information(self, "로그인 성공", "User 로그인 성공!")
        elif id_text == '321' and pw_text == '321':
            QMessageBox.information(self, "로그인 성공", "Staff 로그인 성공!")
        else:
            QMessageBox.warning(self, "로그인 실패", "ID와 PW가 일치하지 않습니다. 다시 로그인해주세요.")

    def show_registration_window(self):
        registration_window = RegistrationWindow(self) 
        registration_window.show()


class RegistrationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 400, 300)
        self.setWindowTitle('회원가입')

        id_label = QLabel('ID:', self)
        self.id_input = QLineEdit(self)

        pw_label = QLabel('PW:', self)
        self.pw_input = QLineEdit(self)
        self.pw_input.setEchoMode(QLineEdit.Password) 

        email_label = QLabel('Email:', self)
        self.email_input = QLineEdit(self)

        name_label = QLabel('Name:', self)
        self.name_input = QLineEdit(self)

        signup_button = QPushButton('가입', self)
        signup_button.clicked.connect(self.signup_button_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(pw_label)
        layout.addWidget(self.pw_input)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(signup_button)

    def signup_button_clicked(self):
        id_text = self.id_input.text()
        pw_text = self.pw_input.text()
        email_text = self.email_input.text()
        name_text = self.name_input.text()

        print(f"ID: {id_text}, PW: {pw_text}, Email: {email_text}, Name: {name_text}")

        self.accept() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
