from PyQt5 import QtWidgets, QtCore 
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import QTimer, QDateTime

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(200, 100, 1133, 731)
        
        # Set gradient background
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(245, 247, 250))
        gradient.setColorAt(1.0, QColor(215, 230, 245))
        palette = self.centralwidget.palette()
        palette.setBrush(QPalette.Window, gradient)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setPalette(palette)
        self.centralwidget.setObjectName("centralwidget")

        # Main vertical layout
        main_vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        main_vertical_layout.setSpacing(0)

        # Navigation bar
        nav_bar = QtWidgets.QWidget()
        nav_bar.setStyleSheet("""
            background-color: rgba(75, 108, 183, 0.9);
            padding: 8px 30px;
            border-bottom: 2px solid #4b6cb7;
        """)
        nav_layout = QtWidgets.QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(20)

        # Date-Time
        self.date_time_label = QtWidgets.QLabel()
        self.date_time_label.setStyleSheet("color: white; font-size: 14px;")
        nav_layout.addWidget(self.date_time_label)

        # Update time every second
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.showTime()

        # Temperature (static for example)
        temp_label = QtWidgets.QLabel("🌡 22°C")
        temp_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        nav_layout.addWidget(temp_label, alignment=QtCore.Qt.AlignCenter)

        # Language selector
        self.lang_combo = QtWidgets.QComboBox()
        self.lang_combo.addItems(["English", "Hindi", "Marathi", "Bengali"])
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #4b6cb7;
                border-radius: 4px;
                padding: 2px 15px 2px 5px;
                min-width: 100px;
                color: #2c3e50;
            }
            QComboBox::drop-down {
                border-left: 1px solid #4b6cb7;
                width: 20px;
            }
        """)
        nav_layout.addWidget(self.lang_combo, alignment=QtCore.Qt.AlignRight)

        main_vertical_layout.addWidget(nav_bar)

        # Main content container
        content_container = QtWidgets.QWidget()
        content_container.setLayout(QtWidgets.QVBoxLayout())
        content_container.layout().setContentsMargins(30, 25, 30, 25)
        content_container.layout().setSpacing(20)

        # Header with title
        header_layout = QtWidgets.QHBoxLayout()
        self.title_label = QtWidgets.QLabel("Dr. NutriEdu")
        self.title_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.title_label.setStyleSheet("""
            color: #2c3e50;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4b6cb7, stop:1 #182848);
            border-radius: 15px;
            color: white;
        """)
        self.title_label.setFixedHeight(60)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        header_layout.addWidget(self.title_label)
        content_container.layout().addLayout(header_layout)

        # Decorative separator
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #4b6cb7;
            height: 3px;
            margin: 10px 50px;
        """)
        content_container.layout().addWidget(separator)

        # Horizontal layout for main content
        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setSpacing(40)

        # Left-side buttons
        left_buttons = [
            ("📅 Book Appointment", "Beat Nutritionist"),
            ("📋 Patient's History", "Solve your Problems"), 
            ("🍎 Meal Suggestions", "Remain Fit")
        ]
        
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.setSpacing(15)
        self.pushBtnAppoinment = self.create_styled_button(*left_buttons[0], "#4b6cb7")
        self.pushBtnDiscuss = self.create_styled_button(*left_buttons[1], "#2c3e50")
        self.pushBtnMeal = self.create_styled_button(*left_buttons[2], "#27ae60")

        for btn in [self.pushBtnAppoinment, self.pushBtnDiscuss, self.pushBtnMeal]:
            left_layout.addWidget(btn)

        # Video widget
        self.video_widget = QVideoWidget(self.centralwidget)
        self.video_widget.setFixedSize(500, 480)
        self.video_widget.setStyleSheet("""
            border: 3px solid #4b6cb7;
            background-color: #ffffff;
            border-radius: 20px;
            padding: 8px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        """)

        # Right-side buttons
        right_buttons = [
            ("📊 Nutritional Values", "Set! Analysis"),
            ("⚖️ Calculate BMI", "Body Mass Index"),
            ("💡 Health Consultation", "Remain Healthy")
        ]
        
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setSpacing(15)
        self.pushBtnNutrition = self.create_styled_button(*right_buttons[0], "#e67e22")
        self.pushBtnCalculateBMI = self.create_styled_button(*right_buttons[1], "#c0392b")
        self.pushBtnHealthConsult = self.create_styled_button(*right_buttons[2], "#16a085")

        for btn in [self.pushBtnNutrition, self.pushBtnCalculateBMI, self.pushBtnHealthConsult]:
            right_layout.addWidget(btn)

        # Add sections to content layout
        content_layout.addLayout(left_layout)
        content_layout.addWidget(self.video_widget, alignment=QtCore.Qt.AlignCenter)
        content_layout.addLayout(right_layout)

        content_container.layout().addLayout(content_layout)

        # Bottom section with back button
        bottom_layout = QtWidgets.QHBoxLayout()
        self.backButton = QtWidgets.QPushButton("◀ Back")
        self.backButton.setFixedSize(140, 45)
        self.backButton.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 16px;
                border-radius: 8px;
                font-weight: bold;
                padding: 8px;
                border: 2px solid #6c757d;
            }
            QPushButton:hover { 
                background-color: #6c757d;
                border-color: #5a6268;
            }
        """)
        bottom_layout.addWidget(self.backButton, alignment=QtCore.Qt.AlignRight)
        content_container.layout().addLayout(bottom_layout)

        main_vertical_layout.addWidget(content_container)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

    def showTime(self):
        current_time = QDateTime.currentDateTime()
        display_text = current_time.toString("dddd, MMMM dd yyyy - hh:mm:ss AP")
        self.date_time_label.setText(display_text)

    def create_styled_button(self, main_text, sub_text, color):
        btn = QtWidgets.QPushButton()
        btn.setText(f"{main_text}\n{sub_text}")
        btn.setFixedHeight(90)
        btn.setFont(QFont("Arial", 12))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {QColor(color).darker(120).name()});
                color: white;
                font-size: 16px;
                border-radius: 12px;
                padding: 12px;
                border: 2px solid {QColor(color).darker(150).name()};
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {QColor(color).darker(130).name()};
                border: 2px solid {QColor(color).darker(180).name()};
            }}
        """)
        return btn

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dr. NutriEdu - Health Kiosk"))