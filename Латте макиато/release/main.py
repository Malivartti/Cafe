__author__ = 'justinarmstrong'

import sqlite3
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QInputDialog
from UI import addEditCoffeeForm
from UI import title


class Add(QWidget):
    def __init__(self, parent=None, number=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.ui = addEditCoffeeForm.Ui_Form2()
        self.ui.setupUi(self)
        self.setWindowTitle('Добавить кофе')
        self.parent = parent
        self.number = number

        self.ui.pushButton_2.hide()
        self.ui.pushButton.clicked.connect(self.table)

    def table(self):
        try:
            con = sqlite3.connect("data\\Cafe.db")
            cur = con.cursor()
            comboBox = ['Необжареный', 'Светлая обжарка', 'Средняя', 'Темная'].index(self.ui.comboBox.currentText()) + 1
            comboBox_2 = ['Молотый', 'В зернах'].index(self.ui.comboBox_2.currentText()) + 1

            cur.execute(f"""INSERT INTO Cofee(ID, Название, Сорт, Степень_обжарки,
             Молотый_В_зернах, Описание_вкуса, Цена, Объем_упаковки) VALUES({self.number + 1}, 
            '{self.ui.lineEdit.text()}', '{self.ui.lineEdit_2.text()}', {comboBox}, {comboBox_2},
            '{self.ui.lineEdit_3.text()}', {self.ui.lineEdit_4.text()}, {self.ui.lineEdit_5.text()})""").fetchall()

            con.commit()
            self.parent.table()
            self.close()
        except:
            self.ui.pushButton.setStyleSheet("QPushButton {background-color: red}")


class Change(QWidget):
    def __init__(self, parent=None, title=None, sort=None, roasting=None, unity=None, intro=None, cost=None, v=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.ui = addEditCoffeeForm.Ui_Form2()
        self.ui.setupUi(self)
        self.setWindowTitle('Изменить кофе')
        self.parent = parent
        self.con = sqlite3.connect("data\\Cafe.db")

        self.title = str(title)
        self.sort = str(sort)
        self.roasting = roasting
        self.unity = unity
        self.intro = str(intro)
        self.cost = cost
        self.v = v

        self.ui.lineEdit.setText(self.title)
        self.ui.lineEdit_2.setText(self.sort)
        self.ui.comboBox.setCurrentText(['Необжареный', 'Светлая обжарка', 'Средняя', 'Темная'][self.roasting - 1])
        self.ui.comboBox_2.setCurrentText(['Молотый', 'В зернах'][self.unity - 1])
        self.ui.lineEdit_3.setText(self.intro)
        self.ui.lineEdit_4.setText(str(cost))
        self.ui.lineEdit_5.setText(str(v))

        self.ui.pushButton.clicked.connect(self.change_line)
        self.ui.pushButton_2.clicked.connect(self.del_line)

    def change_line(self):
        try:
            cur = self.con.cursor()
            comboBox = ['Необжареный', 'Светлая обжарка', 'Средняя', 'Темная'].index(self.ui.comboBox.currentText()) + 1
            comboBox_2 = ['Молотый', 'В зернах'].index(self.ui.comboBox_2.currentText()) + 1

            cur.execute(
                f"""UPDATE Cofee SET Название = '{self.ui.lineEdit.text()}', Сорт = '{self.ui.lineEdit_2.text()}',
             Степень_обжарки = {comboBox}, Молотый_В_зернах = {comboBox_2},
             Описание_вкуса = '{self.ui.lineEdit_3.text()}', Цена = {self.ui.lineEdit_4.text()},
              Объем_упаковки = {self.ui.lineEdit_5.text()} WHERE Название = '{self.title}' """).fetchall()

            self.con.commit()
            self.parent.table()
            self.close()
        except:
            self.ui.pushButton.setStyleSheet("QPushButton {background-color: red}")

    def del_line(self):
        cur = self.con.cursor()
        cur.execute(f'''DELETE from Cofee WHERE Название = '{self.title}' ''').fetchall()
        self.con.commit()
        self.parent.table()
        self.close()


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = title.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Капучино')

        self.bt_add = None
        self.bt_change = None
        self.con = sqlite3.connect("data\\Cafe.db")

        self.table()
        self.ui.add.clicked.connect(self.add_table)
        self.ui.change.clicked.connect(self.change_table)

    def table(self):

        cur = self.con.cursor()
        result = cur.execute('''SELECT * FROM Cofee''').fetchall()
        self.ui.tableWidget.setRowCount(0)
        for i, elem in enumerate(result):
            self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount() + 1)
            for j, val in enumerate(elem):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.ui.tableWidget.resizeColumnsToContents()

    def add_table(self):
        cur = self.con.cursor()
        result = cur.execute('''SELECT Название FROM Cofee''').fetchall()
        self.bt_add = Add(self, len(result))
        self.bt_add.show()

    def change_table(self):
        cur = self.con.cursor()
        result = cur.execute('''SELECT Название FROM Cofee''').fetchall()
        row, ok_pressed = QInputDialog.getItem(
            self, "Выберите вашу страну", "Выберите город:", [str(i[0]) for i in result], 0, False)
        if ok_pressed:
            if cur:
                result = cur.execute(f'''SELECT * FROM Cofee WHERE Название = '{row}' ''').fetchall()
                for i, r in enumerate(result):
                    if i == 0:
                        self.bt_change = Change(self, r[1], r[2], r[3], r[4], r[5], r[6], r[7])
                        self.bt_change.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = Widget()
    root.show()
    sys.exit(app.exec_())
