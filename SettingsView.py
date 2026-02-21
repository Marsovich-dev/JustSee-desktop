
import getpass
import os
import shutil
import config
from Generator import Generator
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from plyer import notification


class SettingsWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(812, 639)
        MainWindow.setStyleSheet("background-color: rgb(50, 50, 50);\n"
                                 "font: 63 12pt \"Cascadia Mono SemiBold\";\n"
                                 "color: rgb(25, 220, 25);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ForceStopButton = QtWidgets.QPushButton(self.centralwidget)
        self.ForceStopButton.setGeometry(QtCore.QRect(490, 560, 241, 51))
        self.ForceStopButton.setObjectName("ForceStopButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 310, 381, 61))
        self.label.setStyleSheet("font: 12pt \"Arial\";")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(490, 500, 241, 51))
        self.StartButton.setObjectName("StartButton")
        self.FilePath = QtWidgets.QLineEdit(self.centralwidget)
        self.FilePath.setGeometry(QtCore.QRect(430, 370, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.FilePath.setFont(font)
        self.FilePath.setStyleSheet("font:12pt \"Arial\";")
        self.FilePath.setObjectName("FilePath")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setGeometry(QtCore.QRect(10, 10, 801, 41))
        font = QtGui.QFont()
        font.setFamily("Cascadia Mono SemiBold")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.Title.setFont(font)
        self.Title.setStyleSheet("font: 63 16pt \"Cascadia Mono SemiBold\";")
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.InputText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.InputText.setGeometry(QtCore.QRect(10, 90, 411, 521))
        font = QtGui.QFont()
        font.setFamily("Cascadia Mono SemiBold")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        font.setKerning(True)
        self.InputText.setFont(font)
        self.InputText.setObjectName("InputText")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(430, 410, 381, 61))
        self.label_2.setStyleSheet("font: 12pt \"Arial\";")
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 381, 21))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(430, 90, 381, 61))
        self.label_4.setStyleSheet("font: 12pt \"Arial\";")
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.inputStartTime = QtWidgets.QTimeEdit(self.centralwidget)
        self.inputStartTime.setGeometry(QtCore.QRect(670, 170, 81, 31))
        self.inputStartTime.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(2, 0, 0)))
        self.inputStartTime.setObjectName("inputStartTime")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(430, 210, 371, 91))
        self.label_6.setStyleSheet("font: 12pt \"Arial\";")
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(430, 170, 221, 31))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.StartButton.clicked.connect(self.__start)
        self.ForceStopButton.clicked.connect(self.__force_stop)

    def __start(self):
        hour, minute = self.inputStartTime.time().hour(), self.inputStartTime.time().minute()
        default_original_img = self.FilePath.text()
        print(default_original_img)
        generator = Generator(self.InputText.toPlainText(), default_original_img, config.img_folder_name)
        generator.generate_wallpapers()
        generator.generate_random_queue(hour, minute)
        generator.write_json()
        self.__add_to_autorun()
        notification.notify(title="Очередь запущена",
                            message=f"Изображения для рабочего стола успешно созданы. Автоматическая смена обоев в {hour}:{"0" * (minute < 10)}{minute} каждого дня.",
                            app_name=config.program_name, timeout=10)


    def __add_to_autorun(self):
        # пишем батник:
        file = open('JustSeeAuto.bat', "w", encoding='cp866')
        print(f"cd /d {os.getcwd()}", file=file)
        print("JustSee.exe -a", file=file)
        file.close()
        username = getpass.getuser()
        dir_name = f'C:/Users/{username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'
        if os.path.exists(dir_name + 'JustSeeAuto.bat'):
            os.remove(dir_name + 'JustSeeAuto.bat')
        shutil.move("JustSeeAuto.bat", dir_name)

    def __force_stop(self):
        username = getpass.getuser()
        dir_name = f'C:/Users/{username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'
        if os.path.exists(dir_name + 'JustSeeAuto.bat'):
            os.remove(dir_name + 'JustSeeAuto.bat')
        notification.notify(title="Автоматическая смена обоев отключена",
                            message="Для возобновления необходимо заново сгенерировать очередь в приложении.",
                            app_name=config.program_name, timeout=10)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", config.program_name + " v" + config.version))
        MainWindow.setWindowIcon(QtGui.QIcon(config.icon))
        self.ForceStopButton.setText(_translate("MainWindow", "Остановить принудительно"))
        self.label.setText(
            _translate("MainWindow", "Путь к файлу, который будет использоваться в качестве исходного фона:"))
        self.StartButton.setText(_translate("MainWindow", "Запустить"))
        self.FilePath.setText(_translate("MainWindow", config.default_original_img))
        self.Title.setText(_translate("MainWindow", config.program_name))
        self.InputText.setPlainText(_translate("MainWindow", "Entertainment - Развлечение\n"
                                                             "Postgraduate - Аспирант"))
        self.label_2.setText(_translate("MainWindow",
                                        "Поверх него будет генерироваться текст со словами и их переводом. Не меняйте для использования фона по умолчанию."))
        self.label_3.setText(_translate("MainWindow", "Словарь:"))
        self.label_4.setText(_translate("MainWindow",
                                        "Пишите словарь по образцу: слово - перевод. Каждая пара на новой строке. Словарь можно скопировать из предложенных в папке Словари."))
        self.label_6.setText(_translate("MainWindow",
                                        "Лучше всего устанавливать время, когда компьютер выключен. Обращаем внимание, что обновление экрана происходит только при следующем включении или перезагрузке."))
        self.label_5.setText(_translate("MainWindow", "Время обновления экрана:"))


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = SettingsWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
