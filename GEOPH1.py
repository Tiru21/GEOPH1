from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from geophoto import Ui_MainWindow
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import sys
import os
import re
import spatialite

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.sOldFileNAme = ""
        self.sNewFileNAme = "НОВОЕ ИМЯ "
        self.sSuffix = "" # расширение
        self.sPath = "" # путь
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButtonDir.clicked.connect(self.pushButtonDirClick)
        self.ui.pushButton1.clicked.connect(self.pushButton1_clicked)
        path = r'C:\Users\w\Documents\PY\python\geoPh\SOURCE'
        #path = QtCore.QDir.currentPath()
        # Объект файловаяМодель
        self.fileModel = QtWidgets.QFileSystemModel(self)
        self.fileModel.setReadOnly(False)
        self.fileModel.setRootPath(path)
        self.fileModel.setFilter(QtCore.QDir.NoDotAndDotDot |  QtCore.QDir.Files)
        self.ui.listView.setModel(self.fileModel)
        self.ui.listView.setRootIndex(self.fileModel.index(path))
        self.ui.listView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ui.listView.clicked.connect(self.listViewClick)
        self.ui.tableWidget.setColumnCount(8)
        self.ui.tableWidget.setRowCount(10)
        self.ui.tableWidget.setHorizontalHeaderLabels(('Дистанция','Тип','Наименование', 'Класс U', 'Часть ВЛ', 'Наименование ВЛ', 'Управляется', 'Подразделение'))
        self.ui.tableWidget.itemClicked.connect(self.tableWidget_clicked)
        self.createConnection("db1.sqlite")
        #self.db = spatialite.connect('db1.sqlite') 
        
    def pushButton1_clicked(self):
        if len(self.ui.lineEditTo.text()) != 0:
            os.rename(self.ui.lineEditFrom.text(), self.ui.lineEditTo.text())

    def tableWidget_clicked(self):
        # обрабатываем клики по таблице и собираем в переменную класса sNewFileNAme новое имя для файла
        self.sNewFileNAme = ""
        t = ""
        for item in self.ui.tableWidget.selectedItems():
            # регулярками оставляем только допустимые для имени файла символы
            t = re.sub('[^-a-zA-Zа-яА-Я0-9_.() ]+', '', item.text()) + " "
            self.sNewFileNAme += t
        self.makeNewName()

    def makeNewName(self):
        # собираем в lineEditTo имя переименования
        if self.sSuffix.upper() in ['JPG', 'JPEG', 'PNG']:
            self.ui.lineEditTo.setText(self.sPath + '/' + self.sNewFileNAme[:-1] + '.' + self.sSuffix)
        else:
            self.ui.lineEditTo.setText("")

    def createConnection(self, namefiledb="db1.sqlite"): # Создаю соединение с базой данных координат опор
        self.db = spatialite.connect(namefiledb)
        self.curr = self.db.cursor()
        
    def get_distance(self, GPSLongitude, GPSLatitude, mDistance=100):
        # Выбираю из базы ближайшие по входящим координатам объекты, заполняю tableWidget
        strsql = f"SELECT Distance(GEOMETRYPLACE, geomfromtext('POINT ({str(GPSLongitude)} {str(GPSLatitude)})', 4326), 1) AS DIST, TYPETM, NAMETM, KLASSVOLTAGE, PARTVL, NAMEVL, MANAGE, DIVISION FROM TECHPLACE WHERE DIST < {mDistance} ORDER BY 1"
        print(strsql)
        #strsql = f"SELECT 22 AS DIST, TYPETM, NAMETM, KLASSVOLTAGE, PARTVL, NAMEVL, MANAGE, DIVISION FROM TECHPLACE LIMIT 6"
        cntrow = 0
        self.ui.tableWidget.clear()
        for row in self.curr.execute(strsql):
            self.ui.tableWidget.setItem(cntrow, 0, QtWidgets.QTableWidgetItem('{0:.2f} м.'.format(row[0])))
            self.ui.tableWidget.setItem(cntrow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.ui.tableWidget.setItem(cntrow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.ui.tableWidget.setItem(cntrow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.ui.tableWidget.setItem(cntrow, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.ui.tableWidget.setItem(cntrow, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.ui.tableWidget.setItem(cntrow, 6, QtWidgets.QTableWidgetItem(row[6]))
            self.ui.tableWidget.setItem(cntrow, 7, QtWidgets.QTableWidgetItem(row[7]))
            cntrow += 1

    def get_geotagging(self, filename):
        # достаю координаты из EXIF файла фотографии
        image = Image.open(filename)
        exif = image._getexif()
        geotagging = {}
        if exif:
            for (idx, tag) in TAGS.items():
                if tag == 'GPSInfo':
                    if idx not in exif:
                        raise ValueError("No EXIF geotagging found")
                    for (key, val) in GPSTAGS.items():
                        if key in exif[idx]:
                            geotagging[val] = exif[idx][key]
        return geotagging

    def get_decimal_from_dms(self, dms, ref):
        # преобразую координаты часы, минуты
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0
        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds
        return round(degrees + minutes + seconds, 5)

    def listViewClick(self):
        self.sNewFileNAme = "НОВОЕ ИМЯ "
        for ix in self.ui.listView.selectedIndexes():
            f = self.fileModel.fileInfo(ix)
            self.sOldFileNAme = f.fileName()
            self.ui.lineEditFrom.setText(f.absoluteFilePath())
            self.sSuffix = f.suffix()
            self.sPath = f.canonicalPath()
            self.makeNewName()

            if str(f.suffix()).upper() in ['JPG', 'JPEG', 'PNG']:
                pixmap = QtGui.QPixmap(f.absoluteFilePath())
                scaled = pixmap.scaled(self.ui.label_2.size(), QtCore.Qt.KeepAspectRatio)
                self.ui.label_2.setPixmap(scaled)
                geot = self.get_geotagging(f.absoluteFilePath())
                if len(geot) != 0:
                    fLatitude = self.get_decimal_from_dms(geot['GPSLatitude'], geot['GPSLatitudeRef'])
                    fLongitude = self.get_decimal_from_dms(geot['GPSLongitude'], geot['GPSLongitudeRef'])
                    self.ui.label.setText(f'{str(fLatitude)}\n{str(fLongitude)}')
                    self.get_distance(str(fLongitude), str(fLatitude), 50)
                else:
                    self.ui.label.setText('Нет геоданных')


    def pushButtonDirClick(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        direct = QtWidgets.QFileDialog.getExistingDirectory(self,"Выберите папку с фотографиями", options=options)
        if direct:
            self.fileModel = QtWidgets.QFileSystemModel(self)
            self.fileModel.setRootPath(direct)
            self.fileModel.setFilter(QtCore.QDir.NoDotAndDotDot |  QtCore.QDir.Files)
            self.ui.listView.setModel(self.fileModel)
            self.ui.listView.setRootIndex(self.fileModel.index(direct))



app = QtWidgets.QApplication([])
win = mywindow()
win.show()
sys.exit(app.exec())
        
