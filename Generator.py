
import shutil
from PIL import Image, ImageFont, ImageDraw
import datetime
import json
import random
import os
import ctypes
import config

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

class Generator:
    def __init__(self, big_line, original_img_path, folder_name, generate_one=False, write_json=True, for_phone=False):
        self.__list_lines = self.get_list_lines(big_line)
        self.__original_img_path = original_img_path
        self.__folder_name = folder_name
        self.__color = (255, 255, 255)
        self.__generate_one = generate_one
        self.__write_json = write_json
        self.__for_phone = for_phone
        self.__queue = {}
        self.__font = None

    def generate_wallpapers(self):
        if self.__folder_name in os.listdir():
            shutil.rmtree(self.__folder_name)
        os.mkdir(self.__folder_name)
        img_id = 0
        for line in self.__list_lines:
            if self.__for_phone:
                img = Image.open(self.__original_img_path)
                draw = ImageDraw.Draw(img)
                text_1 = line[:line.index(" - ")]
                text_2 = line[line.index(" - ") + 3:]
                width, height = img.size
                self.__calculate_font(max(text_1, text_2, key=len), width)
                x = (width - self.__font.getlength(text_1)) / 2
                y = height / 2 - self.__font.size - 10
                draw.text((x, y), text_1, self.__color, self.__font)
                x = (width - self.__font.getlength(text_2)) / 2
                y = height / 2 + 10
                draw.text((x, y), text_2, self.__color, self.__font)

            else:
                img = Image.open(self.__original_img_path)
                img = img.resize((screen_width, int(img.size[1] * (screen_width / img.size[0]))))   # чтобы текст не пришось уменьшать, масштабируем изображение по ширине экрана
                indent_height = (img.size[1] - screen_height) / 2
                img = img.crop((0, indent_height, img.size[0], img.size[1] - indent_height))    # а высоту срезаем. Отстаётся то, что по центру.

                # img = img.resize((screen_width*(screen_height/img.size[1]), screen_height))
                # indent_width = (img.size[0] - screen_width)/2
                # img.crop((indent_width, 0, img.size[0]-indent_width, img.size[1]))
                draw = ImageDraw.Draw(img)
                width, height = img.size
                self.__calculate_font(line, width)
                x = (width - self.__font.getlength(line)) / 2
                y = height - self.__font.size - 48 - 30
                draw.text((x, y), line, self.__color, self.__font)
            img.save(f"{self.__folder_name}\image_{img_id}.png")
            img_id += 1

            if self.__generate_one:
                print("one, ok")
                return None
        print("All generated")

    def generate_random_queue(self, target_hours, target_minutes):
        images = [i for i in os.listdir(self.__folder_name)]
        random.shuffle(images)
        start_date = {"year": datetime.datetime.now().date().year,
                      "month": datetime.datetime.now().date().month,
                      "day": datetime.datetime.now().date().day }
        for i in range(len(images)):
            target_datetime = datetime.datetime(**start_date) + datetime.timedelta(days=i+1, hours=target_hours, minutes=target_minutes)
            self.__queue[i] = {"datetime": {"year": target_datetime.year,
                                            "month": target_datetime.month,
                                            "day": target_datetime.day,
                                            "hour": target_datetime.hour,
                                            "minute": target_datetime.minute},
                               "image": images[i]}

    def write_json(self):
        with open("queue.json", "w", encoding="utf-8") as file:
            json.dump(self.__queue, file, indent=4, ensure_ascii=False)
        with open("last_change.json", "w", encoding="utf-8") as file:
            json.dump({"id": -1}, file, indent=4, ensure_ascii=False)

    def auto_select_color(self):
        pass

    def __calculate_font(self, line, img_width):
        for font_size in range(100, 10, -1):
            self.__font = ImageFont.truetype(config.font, font_size)
            if self.__font.getlength(line) <= img_width - 30 * (not self.__for_phone) - 100 * self.__for_phone:
                break

    def get_list_lines(self, big_line):
        list_lines = []
        old_index = 0
        for i in range(len(big_line)):
            if big_line[i] == "\n":
                list_lines.append(big_line[old_index:i])
                old_index = i + 1
            if i == len(big_line) - 1:
                list_lines.append(big_line[old_index:i + 1])
                old_index = i + 1
        while "" in list_lines: list_lines.remove("")
        while " " in list_lines: list_lines.remove(" ")
        print(list_lines)
        return list_lines



if __name__ == "__main__":
    text = """Introduce - Внедрять
revise - пересматривать 
diverse - разнообразный
elections - выборы
Power - Власть 
to reject a law - отклонять закон 
term - срок
Emergency - появление
Establish - создавать, учреждать 
To rule - править 
appoint - назначать 
Invade - вторгаться 
Conquer - завоёвывать 
Fight - Битва
achieve - достигать
freedom - свобода 
independence - независимость 
several - несколько"""
    g = Generator(text, "img/original (phone).png", "Set 4", write_json=False, for_phone=True)
    # g = Generator(text, "img/original.jpg", "Set 2", write_json=False)
    g.generate_wallpapers()
    # g.generate_random_queue(2, 0)
    # g.write_json()
