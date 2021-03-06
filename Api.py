import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFocus()
        uic.loadUi('1.ui', self)
        self.setWindowTitle('MapApi')
        self.buttonGroup.buttonClicked.connect(self.generate)
        self.radioButton_3.clicked.connect(self.generate)
        self.radioButton_4.clicked.connect(self.generate)
        self.type = False
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.vipe)
        self.checkBox.clicked.connect(self.search)
        self.center = [301, 211]

    def keyPressEvent(self, event):
        global map_params
        if event.key() == Qt.Key_PageDown:
            if float(map_params['spn'].split(',')[0]) * 1.1 < 40 and \
                    float(map_params['spn'].split(',')[1]) * 1.1 < 40:
                map_params['spn'] = ','.join([str(float(map_params['spn'].split(',')[0]) * 1.1),
                                              str(float(map_params['spn'].split(',')[1]) * 1.1)])
        elif event.key() == Qt.Key_PageUp:
            if float(map_params['spn'].split(',')[0]) * 0.1 > 0.001 and \
                    float(map_params['spn'].split(',')[1]) * 0.1 > 0.001:
                map_params['spn'] = ','.join([str(float(map_params['spn'].split(',')[0]) * 0.1),
                                              str(float(map_params['spn'].split(',')[1]) * 0.1)])
        elif event.key() == Qt.Key_Up:
            map_params['ll'] = ','.join([str(float(map_params['ll'].split(',')[0])),
                                         str(float(map_params['ll'].split(',')[1]) +
                                             float(map_params['spn'].split(',')[0]))])
        elif event.key() == Qt.Key_Down:
            map_params['ll'] = ','.join(
                [str(float(map_params['ll'].split(',')[0])),
                 str(float(map_params['ll'].split(',')[1]) -
                     float(map_params['spn'].split(',')[0]))])
        elif event.key() == Qt.Key_Right:
            map_params['ll'] = ','.join(
                [str(float(map_params['ll'].split(',')[0]) +
                     float(map_params['spn'].split(',')[0])),
                 str(float(map_params['ll'].split(',')[1]))])
        elif event.key() == Qt.Key_Left:
            map_params['ll'] = ','.join(
                [str(float(map_params['ll'].split(',')[0]) -
                     float(map_params['spn'].split(',')[0])),
                 str(float(map_params['ll'].split(',')[1]))])
        request()

    def mousePressEvent(self, event):
        global map_params
        if event.button() == Qt.LeftButton:
            if 0 <= int(event.x()) <= 601 and 0 <= int(event.y()) <= 421:
                coords = [int(event.x()), int(event.y())]
                rotate = [(coords[0] - self.center[0]) / 180 *
                          float(map_params['spn'].split(',')[0]),
                          (coords[1] - self.center[1]) / 320 *
                          float(map_params['spn'].split(',')[0])]
                t_long, t_lat = float(map_params['ll'].split(',')[0]), \
                                                       float(map_params['ll'].split(',')[1])
                map_params[
                    'pt'] = f"{','.join([str(t_long + rotate[0]), str(t_lat - rotate[1])])},flag"
                map_params[
                    'll'] = f"{','.join([str(t_long + rotate[0]), str(t_lat - rotate[1])])}"
            else:
                return
            self.search()
        elif event.button() == Qt.RightButton:
            if 0 <= int(event.x()) <= 601 and 0 <= int(event.y()) <= 421:
                coords = [int(event.x()), int(event.y())]
                rotate = [(coords[0] - self.center[0]) / 180 *
                          float(map_params['spn'].split(',')[0]),
                          (coords[1] - self.center[1]) / 320 *
                          float(map_params['spn'].split(',')[0])]
                t_long, t_lat = float(map_params['ll'].split(',')[0]), float(map_params['ll'].split(
                    ',')[1])
                map_params[
                    'pt'] = f"{','.join([str(t_long + rotate[0]), str(t_lat - rotate[1])])},flag"
                self.serch_org()
            else:
                return

    def generate(self):
        global map_params
        for button in self.buttonGroup.buttons():
            if button.isChecked():
                map_params['l'] = button.text()
                if button.text() == 'sat':
                    self.type = True
                else:
                    self.type = False
        if self.radioButton_4.isChecked():
            map_params['l'] += f',{self.radioButton_4.text()}'
        if self.radioButton_3.isChecked():
            map_params['l'] += f',{self.radioButton_3.text()}'
        request()

    def search(self):
        self.label.setFocus()
        global map_params
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        if self.sender() is None:
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": map_params['ll'],
                "format": "json"}
        else:
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": self.lineEdit.text(),
                "format": "json"}
        try:
            response = requests.get(geocoder_api_server, params=geocoder_params)
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            address = toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
            try:
                index = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
            except Exception:
                self.checkBox.setCheckState(False)
            toponym_coodrinates = toponym["Point"]["pos"]
            toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        except Exception:
            self.textBrowser.setPlainText('Ничего не найдено!')
            return
        map_params['ll'] = ','.join([toponym_longitude, toponym_lattitude])
        map_params['pt'] = f"{','.join([toponym_longitude, toponym_lattitude])}" \
                           f",flag"
        self.textBrowser.setPlainText('\n'.join(address.split(', ')))
        if self.checkBox.isChecked():
            self.textBrowser.setPlainText('\n'.join(address.split(', ')) + '\n' + index)
        else:
            self.textBrowser.setPlainText('\n'.join(address.split(', ')))
        request()

    def serch_org(self):
        global map_params
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": map_params['pt'][:-5],
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        response = response.json()
        toponym = response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        address = ','.join(toponym['metaDataProperty']['GeocoderMetaData'][
                               'Address']['formatted'].split(', '))
        search_map_params = {
            'apikey': 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
            'text': address,
            'lang': 'ru_RU',
            "ll": map_params['pt'][:-5],
            'type': 'biz',
            "spn": '0.0008,0.0008',
            'rspn': '1'}

        map_search_server = "https://search-maps.yandex.ru/v1/"
        # ... и выполняем запрос
        response = requests.get(map_search_server, params=search_map_params)
        response = response.json()
        try:
            time = response["features"][0]["properties"]['CompanyMetaData']['Hours']['text']
            name = response["features"][0]["properties"]['name']
            address = response["features"][0]["properties"]['description']
            self.textBrowser.setPlainText('\n'.join([name, address, time]))
        except Exception:
            self.textBrowser.setPlainText('Ничего не найдено!')
            return

    def vipe(self):
        global map_params
        map_params.pop('pt', None)
        self.lineEdit.setText('')
        self.textBrowser.setPlainText('')
        request()

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


def request():
    response = requests.get(server, params=map_params)
    if response:
        if not ex.type:
            map_file = "map.png"
        else:
            map_file = 'map.jpg'
        with open(map_file, "wb") as file:
            file.write(response.content)
            ex.load_image(map_file)
    else:
        print("Ошибка выполнения запроса:")


request()
ex.show()
sys.exit(app.exec_())
