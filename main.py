import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox, QVBoxLayout, QHBoxLayout, QDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from db import check_login_User, check_login_Staff, register_new_user, register_new_car, delete_car, get_car_data, get_staff_name, check_accident, reserve_car, show_reserver

class MyWindow(QWidget):
    
    current_user = None
    
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(800, 300, 800, 600)
        self.setWindowTitle('DBS: Term Project')

        self.banner_label = QLabel(self)
        self.banner_label.setGeometry(0, 0, self.width(), 50)
        self.banner_label.setStyleSheet("background-color: #4CAF50; color: white;")
        self.banner_label.setAlignment(Qt.AlignCenter)
        self.banner_label.setFont(QFont('Arial', 20))
        self.banner_label.setText("중고차 매매 시스템")

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

        self.user_window = UserWindow()
        self.staff_window = StaffWindow()
        self.registration_window = RegistrationWindow(self)

        self.show()

    def login_button_clicked(self):
        id_text = self.id_input.text()
        pw_text = self.pw_input.text()

        if check_login_User(id_text, pw_text):
            QMessageBox.information(self, "로그인 성공", "User 로그인 성공!")
            MyWindow.current_user = {'id': id_text, 'role': 'user'}
            print(self.current_user)
            self.hide()
            self.show_user_window()
        elif check_login_Staff(id_text, pw_text):
            QMessageBox.information(self, "로그인 성공", "Staff 로그인 성공!")
            MyWindow.current_user = {'id': id_text, 'role': 'staff'}
            self.hide()
            self.show_staff_window()
        else:
            QMessageBox.warning(self, "로그인 실패", "ID와 PW가 일치하지 않습니다. 다시 로그인해주세요.")
            self.clear_inputs()

    def show_registration_window(self):
        self.registration_window.exec_()

    def hide_registration_widgets(self):
        self.id_label.hide()
        self.id_input.hide()
        self.pw_label.hide()
        self.pw_input.hide()

        try:
            self.signup_button.hide()
        except AttributeError:
            pass
        
    def clear_inputs(self):
        self.id_input.clear()
        self.pw_input.clear()

    
    def show_user_window(self):
        self.user_window = UserWindow()
        self.user_window.show()

    def show_staff_window(self):
        self.staff_window = StaffWindow()
        self.staff_window.show()


# 회원가입 window
class RegistrationWindow(QDialog):

    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = MyWindow.current_user  
        self.initUI()

    def initUI(self):
        self.setGeometry(900, 400, 400, 300)
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

    def clear_inputs(self):
        self.id_input.clear()
        self.pw_input.clear()
        self.email_input.clear()
        self.name_input.clear()

    def signup_button_clicked(self):
        id_text = self.id_input.text()
        pw_text = self.pw_input.text()
        email_text = self.email_input.text()
        name_text = self.name_input.text()
        
        if register_new_user(id_text,pw_text,email_text,name_text)==True:
            print(f"ID: {id_text}, PW: {pw_text}, Email: {email_text}, Name: {name_text}")
            self.accept() 
        
        else:
            QMessageBox.warning(self, "회원가입 실패", "해당 ID가 이미 사용중입니다.")
            self.clear_inputs() 
            self.show() 
            

        
        
# 사용자 window
class UserWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = MyWindow.current_user
        self.sort_count = {'price': 0, 'distance': 0, 'age': 0}
        self.current_data_index = 0
        self.initUI()
        
    def initUI(self):
        self.setGeometry(800, 300, 800, 600)
        self.setWindowTitle('DBS: Term Project - User Window')

        self.banner_label = QLabel(self)
        self.banner_label.setGeometry(0, 0, self.width(), 50)
        self.banner_label.setStyleSheet("background-color: #4CAF50; color: white;")
        self.banner_label.setAlignment(Qt.AlignCenter)
        self.banner_label.setFont(QFont('Arial', 20))
        self.banner_label.setText("중고차 매매 시스템 - User")
        
        self.car_data = get_car_data()
        
        self.image_label = QLabel(self)
        self.model_label = QLabel(self)
        self.sid_label = QLabel(self)
        self.price_label = QLabel(self)
        self.age_label = QLabel(self)
        self.distance_label = QLabel(self)

        self.display_current_data()
        
        reserve_button = QPushButton('예약하기', self)
        reserve_button.setGeometry(250, 500, 100, 30)
        reserve_button.clicked.connect(self.reserve_button_clicked)
        
        search_button = QPushButton('조회하기', self)
        search_button.setGeometry(450, 500, 100, 30)
        search_button.clicked.connect(self.search_button_clicked)

        left_arrow_button = QPushButton('←', self)
        right_arrow_button = QPushButton('→', self)

        button_width = 240
        button_height = 20
        arrow_button_width = 50


        left_arrow_button.clicked.connect(self.left_arrow_clicked)
        right_arrow_button.clicked.connect(self.right_arrow_clicked)

        left_arrow_button.setGeometry(0, 60, arrow_button_width, button_height)
        right_arrow_button.setGeometry(750, 60, arrow_button_width, button_height)
        
    def display_current_data(self):
        current_car = self.car_data[self.current_data_index]

        image_path = 'C://Users//user//Desktop//DBS_TermProject//Database 생성//image//' + current_car['image']
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"이미지를 로드할 수 없습니다. 경로: {image_path}")
        else:
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setGeometry(20, 100, 400, 300)
                
        seller_name = current_car['seller']
        staff_name = get_staff_name(seller_name)

        self.model_label.setText('차량 : ' + current_car['model'])
        if staff_name:
            self.sid_label.setText('판매자 : ' + staff_name + ' 딜러')
        else:
            self.sid_label.setText('판매자 : ' + seller_name + ' 딜러')
        self.price_label.setText('가격 : ' + str(current_car['price']) + ' 만원')
        self.age_label.setText(str(current_car['age']) + '년식')
        self.distance_label.setText(str(current_car['distance']) + 'km')


        font = QFont('고딕')
        font.setPointSize(18)  
        self.model_label.setFont(font)
        self.model_label.setAlignment(Qt.AlignCenter) 
        self.model_label.setGeometry(450, 120, 310, 60)
        
        self.sid_label.setFont(font)
        self.sid_label.setAlignment(Qt.AlignCenter) 
        self.sid_label.setGeometry(450, 200, 310, 60)
        
        self.price_label.setFont(font)
        self.price_label.setAlignment(Qt.AlignCenter) 
        self.price_label.setGeometry(450, 280, 310, 60)
        
        self.age_label.setFont(font)
        self.age_label.setAlignment(Qt.AlignCenter) 
        self.age_label.setGeometry(450, 345, 155, 60)
        
        self.distance_label.setFont(font)
        self.distance_label.setAlignment(Qt.AlignCenter) 
        self.distance_label.setGeometry(605, 345, 155, 60)

    def left_arrow_clicked(self):
        if self.current_data_index > 0:
            self.current_data_index -= 1
            self.display_current_data()
        else:
            msg_box = QMessageBox()
            msg_box.setText("더 이상 이전 데이터가 없습니다.")
            msg_box.exec_()

    def right_arrow_clicked(self):
        if self.current_data_index < len(self.car_data) - 1:
            self.current_data_index += 1
            self.display_current_data()
        else:
            msg_box = QMessageBox()
            msg_box.setText("더 이상 다음 데이터가 없습니다.")
            msg_box.exec_()

    def reserve_button_clicked(self):
        msg_box = QMessageBox()
        msg_box.setText("예약이 완료되었습니다.")
        current_car = self.car_data[self.current_data_index]
        cid_to_reserve = current_car['cid'] 
        reserve_car(cid_to_reserve,self.current_user['id'])
        msg_box.exec_()

    def search_button_clicked(self):
        current_car = self.car_data[self.current_data_index]
        cid_to_check = current_car['cid'] 

        result = check_accident(cid_to_check)

        msg_box = QMessageBox()

        if not result:
            msg_box.setText("무사고 차량입니다.")
        else:
            accident_info = "\n".join([f"사고 번호: {accident['anum']}, 사고 일자: {accident['adate']}" for accident in result[1]])
            msg_box.setText(f"해당 차량은 사고가 있습니다. \n{accident_info}")


        msg_box.exec_()
        
        
        
        
class StaffWindow(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = MyWindow.current_user  
        self.initUI()

    def initUI(self):
        self.setGeometry(800, 300, 800, 600)
        self.setWindowTitle('DBS: Term Project - Staff Window')

        self.banner_label = QLabel(self)
        self.banner_label.setGeometry(0, 0, self.width(), 50)
        self.banner_label.setStyleSheet("background-color: #4CAF50; color: white;")
        self.banner_label.setAlignment(Qt.AlignCenter)
        self.banner_label.setText("중고차 매매 시스템 - Staff")

        register_button = QPushButton('Register', self)
        delete_button = QPushButton('Delete', self)
        show_button = QPushButton('Show', self)
        
        button_width = 200
        button_height = 100
        register_button.setFixedSize(button_width, button_height)
        delete_button.setFixedSize(button_width, button_height)
        show_button.setFixedSize(button_width, button_height)

        register_button.clicked.connect(self.show_registration_car_window)
        delete_button.clicked.connect(self.show_delete_car_window)
        show_button.clicked.connect(self.show_show_car_window)

        hbox = QHBoxLayout()
        hbox.addWidget(register_button)
        hbox.addWidget(delete_button)
        hbox.addWidget(show_button)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
        
    def show_registration_car_window(self):
        registration_car_window = RegistrationCarWindow(self)
        registration_car_window.exec_()
        
    def show_delete_car_window(self):
        delete_car_window = DeleteCarWindow(self)
        delete_car_window.exec_()
    
    def show_show_car_window(self):
        result = show_reserver(self.current_user['id'])

        msg_box = QMessageBox()

        if not result:
            msg_box.setText("예약이 없습니다.")
        else:
            reservation_info = "\n".join([f"예약자 아이디: {info['uid']}, 예약자 이름: {info['user_name']}, 예약자 연락처: {info['email']}, 차량 번호: {info['cid']}, 차량 모델: {info['model']}" for info in result])
            msg_box.setText(f"예약 정보입니다. \n{reservation_info}")

        msg_box.exec_()
        
    

class RegistrationCarWindow(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = MyWindow.current_user 
        self.initUI()

    def initUI(self):
        self.setGeometry(900, 400, 400, 300)
        self.setWindowTitle('중고차 등록')

        cid_label = QLabel('CID:', self)
        self.cid_input = QLineEdit(self)

        age_label = QLabel('Age:', self)
        self.age_input = QLineEdit(self)

        model_label = QLabel('Model:', self)
        self.model_input = QLineEdit(self)

        distance_label = QLabel('Distance:', self)
        self.distance_input = QLineEdit(self)

        price_label = QLabel('Price:', self)
        self.price_input = QLineEdit(self)

        image_label = QLabel('Image:', self)
        self.image_input = QLineEdit(self)

        register_button = QPushButton('등록', self)
        register_button.clicked.connect(self.register_button_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(cid_label)
        layout.addWidget(self.cid_input)
        layout.addWidget(age_label)
        layout.addWidget(self.age_input)
        layout.addWidget(model_label)
        layout.addWidget(self.model_input)
        layout.addWidget(distance_label)
        layout.addWidget(self.distance_input)
        layout.addWidget(price_label)
        layout.addWidget(self.price_input)
        layout.addWidget(image_label)
        layout.addWidget(self.image_input)
        layout.addWidget(register_button)

    def clear_inputs(self):
        self.cid_input.clear()
        self.age_input.clear()
        self.model_input.clear()
        self.distance_input.clear()
        self.price_input.clear()
        self.image_input.clear()

    def register_button_clicked(self):
        cid_text = self.cid_input.text()
        age_text = self.age_input.text()
        model_text = self.model_input.text()
        distance_text = self.distance_input.text()
        price_text = self.price_input.text()
        image_text = self.image_input.text()

        if register_new_car(cid_text, age_text, model_text,self.current_user['id'], distance_text, price_text, image_text) == True:
            print(f"CID: {cid_text}, Age: {age_text}, Model: {model_text}, Staff: {self.current_user['id']}, Distance: {distance_text}, Price: {price_text}, Image: {image_text}")
            self.accept()
        else:
            QMessageBox.warning(self, "등록 실패", "차량 등록에 실패했습니다.")
            self.clear_inputs()
            self.show()

class DeleteCarWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(900, 400, 400, 150)
        self.setWindowTitle('중고차 삭제')

        cid_label = QLabel('삭제하실 차량 번호를 입력해주세요:', self)
        self.cid_input = QLineEdit(self)

        delete_button = QPushButton('삭제', self)
        delete_button.clicked.connect(self.delete_button_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(cid_label)
        layout.addWidget(self.cid_input)
        layout.addWidget(delete_button)

    def delete_button_clicked(self):
        cid_text = self.cid_input.text()
        confirm_message = f'정말로 차량 번호 {cid_text} 차량을 삭제하시겠습니까?\n(해당 데이터는 영구히 삭제됩니다.)'
        reply = QMessageBox.question(self, '삭제 확인', confirm_message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if delete_car(cid_text):
                QMessageBox.information(self, '삭제 완료', '차량이 삭제되었습니다.')
                
            else:
                QMessageBox.warning(self, '삭제 실패', '차량 번호를 다시 확인해주세요.')
            
            self.accept()
            
        else:
            self.reject()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
