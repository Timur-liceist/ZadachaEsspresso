import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QTableWidgetItem

from untitled import Ui_MainWindow


class RedactWindow(QMainWindow):
    def __init__(self, tableWidget, sort_coff, obzharka, moloti, opis, cennik, obiem, id):
        super().__init__()
        self.tableWidget = tableWidget
        uic.loadUi("addEditCoffeeForm.ui", self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = list(map(lambda x: x[0], cur.execute("""SELECT title FROM sorts_coffee""").fetchall()))
        self.name_sort.addItems(result)
        self.button_add.setText("Сохранить")
        self.button_add.clicked.connect(self.run)
        self.cancel.clicked.connect(self.close)
        self.cena.setValue(int(cennik))
        self.obem.setValue(int(obiem))
        self.name_sort.setCurrentText(sort_coff)
        self.molot.setCurrentText(moloti)
        self.opisanie.setText(opis)
        self.stepen_obzharki.setCurrentText(obzharka)
        self.show()
        self.id = id

    def run(self):
        self.close()
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""UPDATE coffee SET name_sort = (SELECT id FROM sorts_coffee WHERE title = '{self.name_sort.currentText()}'),
         obzharka = (SELECT id FROM stepen_obzharki WHERE title = '{self.stepen_obzharki.currentText()}'),
          moloti = (SELECT id FROM type_coffee WHERE title = '{self.molot.currentText()}'),
           opisanie = '{self.opisanie.text()}',
cena = {self.cena.text()},
obem = {self.obem.text()} WHERE ID = {self.id}""")
        self.tableWidget.setRowCount(0)
        index = 0
        result = cur.execute(f"""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for i in result:
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(i[0])))
            # for j in range(1, 4):
            t = cur.execute(f"""SELECT title FROM sorts_coffee WHERE id = {i[1]}""").fetchall()[0][0]
            self.tableWidget.setItem(index, 1, QTableWidgetItem(t))
            t = cur.execute(f"""SELECT title FROM stepen_obzharki WHERE id = {i[2]}""").fetchall()[0][0]
            self.tableWidget.setItem(index, 2, QTableWidgetItem(t))
            t = cur.execute(f"""SELECT title FROM type_coffee WHERE id = {i[3]}""").fetchall()[0][0]
            self.tableWidget.setItem(index, 3, QTableWidgetItem(t))
            for j in range(4, 7):
                self.tableWidget.setItem(index, j, QTableWidgetItem(str(i[j])))
            index += 1
        con.commit()
        con.close()


class AddingWindow(QMainWindow):
    def __init__(self, tableWidget):
        super().__init__()
        self.tableWidget = tableWidget
        uic.loadUi("addEditCoffeeForm.ui", self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = list(map(lambda x: x[0], cur.execute("""SELECT title FROM sorts_coffee""").fetchall()))
        self.name_sort.addItems(result)
        self.button_add.clicked.connect(self.run)
        self.cancel.clicked.connect(self.close)
        self.show()

    def run(self):
        self.close()
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        cur.execute(
            f"""INSERT INTO coffee VALUES(NULL, (SELECT id FROM sorts_coffee WHERE title = '{self.name_sort.currentText()}'), (SELECT id FROM stepen_obzharki WHERE title = '{self.stepen_obzharki.currentText()}'), (SELECT id FROM type_coffee WHERE title = '{self.molot.currentText()}'), '{self.opisanie.text()}', {self.cena.text()}, {self.obem.text()})""")
        self.tableWidget.setRowCount(0)
        index = 0
        result = cur.execute(f"""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for i in result:
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(i[0])))
            # for j in range(1, 4):
            t = cur.execute(f"""SELECT title FROM sorts_coffee WHERE id = {i[1]}""").fetchall()[0][0]
            self.tableWidget.setItem(index, 1, QTableWidgetItem(t))
            t = cur.execute(f"""SELECT title FROM stepen_obzharki WHERE id = {i[2]}""").fetchall()[0][0]
            self.tableWidget.setItem(index, 2, QTableWidgetItem(t))
            t = cur.execute(f"""SELECT title FROM type_coffee WHERE id = {i[3]}""").fetchall()[0][0]
            self.tableWidget.setItem(index, 3, QTableWidgetItem(t))
            for j in range(4, 7):
                self.tableWidget.setItem(index, j, QTableWidgetItem(str(i[j])))
            index += 1
        con.commit()
        con.close()


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        # self.setupUi(self)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 120)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        self.add.clicked.connect(self.adding)
        index = 0
        result = cur.execute(f"""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for i in result:
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(i[0])))
            # for j in range(1, 4):
            t = cur.execute(f"""SELECT title FROM sorts_coffee WHERE id = {i[1]}""").fetchall()[0][0]
            self.tableWidget.setItem(index, 1, QTableWidgetItem(t))
            t = cur.execute(f"""SELECT title FROM stepen_obzharki WHERE id = {i[2]}""").fetchall()[0][0]
            self.tableWidget.setItem(index, 2, QTableWidgetItem(t))
            t = cur.execute(f"""SELECT title FROM type_coffee WHERE id = {i[3]}""").fetchall()[0][0]
            self.tableWidget.setItem(index, 3, QTableWidgetItem(t))
            for j in range(4, 7):
                self.tableWidget.setItem(index, j, QTableWidgetItem(str(i[j])))
            index += 1
        self.redact.clicked.connect(self.redacting)
        con.close()

    def adding(self):
        self.window = AddingWindow(self.tableWidget)

    def redacting(self):
        current = self.tableWidget.currentRow()
        self.window = RedactWindow(self.tableWidget, self.tableWidget.item(current, 1).text(),
                                   self.tableWidget.item(current, 2).text(), self.tableWidget.item(current, 3).text(),
                                   self.tableWidget.item(current, 4).text(), self.tableWidget.item(current, 5).text(),
                                   self.tableWidget.item(current, 6).text(), self.tableWidget.item(current, 0).text())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Window()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
