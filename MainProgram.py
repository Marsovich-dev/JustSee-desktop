
import ctypes
import datetime
import json
import os
import sys
import config
from plyer import notification
from SettingsView import SettingsWindow
from PyQt5 import QtWidgets


class MainProgram:
    def __init__(self):
        self.__app = QtWidgets.QApplication(sys.argv)
        self.__MainWindow = QtWidgets.QMainWindow()
        self.__ui = SettingsWindow()
        self.__ui.setupUi(self.__MainWindow)
        # self.last_change = {"id": 0}
        with open("queue.json", "r", encoding="utf-8") as file:
            self.queue = json.load(file)

    def view(self):
        self.__MainWindow.show()
        sys.exit(self.__app.exec_())

    def update(self):
        self.read_last_change()
        last_id = self.last_change["id"]
        if last_id + 1 >= len(self.queue):
            if datetime.datetime.now() >= datetime.datetime(**self.queue[str(last_id)]["datetime"]) + datetime.timedelta(days=1):   # сообщение выводится только на следующий день после последнего изображения.
                notification.notify("Очередь обоев закончилась", "Фон рабочего стола больше не будет меняться автоматически. Перейдите в главное окно программы (с настройками), чтобы создать новую очередь.",
                                    app_name=config.program_name, timeout=20)

        elif datetime.datetime.now() >= datetime.datetime(**self.queue[str(last_id+1)]["datetime"]):
            current_id = last_id + 1
            self.change_wallpaper(os.path.abspath(f"{config.img_folder_name}/{self.queue[str(current_id)]["image"]}"))
            self.last_change["id"] = current_id
            self.write_last_change()

    def read_last_change(self):
        with open("last_change.json", "r", encoding="utf-8") as file:
            self.last_change = json.load(file)

    def write_last_change(self):
        with open("last_change.json", "w", encoding="utf-8") as file:
            json.dump(self.last_change, file, indent=4, ensure_ascii=False)

    def change_wallpaper(self, image_path: str):
        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDWININICHANGE = 0x02
        try:
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path,
                                                       SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
            print("Succes change_wallpaper")
        except Exception as e:
            print(f"Error changing wallpaper: {e}")

