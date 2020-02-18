import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('1.ui', self)

    def load_image(self, image):
        self.pixmap = QPixmap(image)
        self.label.setPixmap(self.pixmap)


app = QApplication(sys.argv)
ex = MyWidget()

server = 'https://static-maps.yandex.ru/1.x/'
map_params = {
    'll': '37.795384,55.694768',
    'spn': '0.5,0.5',
    'l': 'map'
}

response = requests.get(server, params=map_params)
if response:
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
        ex.load_image(map_file)
    os.remove(map_file)
else:
    print("Ошибка выполнения запроса:")

ex.show()
sys.exit(app.exec_())
