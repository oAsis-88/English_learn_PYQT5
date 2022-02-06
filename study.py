import json
import re
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtGui import QPalette, QColor
from numpy import random
from SQL_query import englishWords


class Ui_Dialog(object):
    def setupUi(self, Main):
        Main.setObjectName("Dialog")
        Main.resize(800, 450)
        # Main.setWindowFlag(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        # Main.setWindowFlag(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)
        # Main.setWindowOpacity(0.85)
        ico = QtGui.QIcon("image/icon_sleep.jpg")
        Main.setWindowIcon(ico)
        pal = Main.palette()
        pal.setColor(QtGui.QPalette.Active, QtGui.QPalette.Window, QtGui.QColor("#4068a0"))
        pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QColor("#409ba0"))
        Main.setPalette(pal)

        font_btn = QtGui.QFont()
        font_btn.setFamily("Arial")
        font_btn.setPointSize(12)

        font_word = QtGui.QFont()
        font_word.setFamily("Arial")
        font_word.setPointSize(50)

        self.box_language_QRadioButton = QtWidgets.QVBoxLayout()
        self.en_ru = QtWidgets.QRadioButton("en_ru")
        self.en_ru.setChecked(True)
        self.ru_en = QtWidgets.QRadioButton("ru_en")
        self.box_language_QRadioButton.addWidget(self.en_ru, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.box_language_QRadioButton.addWidget(self.ru_en, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.box_word_QLabel = QtWidgets.QHBoxLayout()
        self.word = QtWidgets.QLabel("1")
        self.word.setFont(font_word)
        self.word2 = QtWidgets.QLabel("2")
        self.word2.setFont(font_word)
        self.word3 = QtWidgets.QLabel("3")
        self.word3.setFont(font_word)
        self.box_word_QLabel.addWidget(self.word, alignment=QtCore.Qt.AlignHCenter)
        self.box_word_QLabel.addWidget(self.word2, alignment=QtCore.Qt.AlignHCenter)
        self.box_word_QLabel.addWidget(self.word3, alignment=QtCore.Qt.AlignHCenter)
        self.box_word_QLabel.setSpacing(50)

        self.box_input_QLineEdit = QtWidgets.QHBoxLayout()
        self.input = QtWidgets.QLineEdit()
        self.input.setFont(font_word)
        self.input2 = QtWidgets.QLineEdit()
        self.input2.setFont(font_word)
        self.input3 = QtWidgets.QLineEdit()
        self.input3.setFont(font_word)
        self.box_input_QLineEdit.addWidget(self.input)
        self.box_input_QLineEdit.addWidget(self.input2)
        self.box_input_QLineEdit.addWidget(self.input3)
        self.box_input_QLineEdit.setSpacing(10)

        self.box_button_QPushButton = QtWidgets.QHBoxLayout()
        self.check_word = QtWidgets.QPushButton("Проверить")
        self.check_word.setFont(font_btn)
        self.update_word = QtWidgets.QPushButton("Обновить")
        self.update_word.setFont(font_btn)
        self.box_button_QPushButton.addWidget(self.check_word)
        self.box_button_QPushButton.addWidget(self.update_word)
        self.box_button_QPushButton.setSpacing(10)

        # self.all_boxl = QtWidgets.QVBoxLayout(Main)
        # self.all_boxl.addLayout(self.box_language_QRadioButton)
        # self.all_boxl.addLayout(self.box_word_QLabel)
        # self.all_boxl.addLayout(self.box_input_QLineEdit)
        # self.all_boxl.addLayout(self.box_button_QPushButton)

        self.all_box = QtWidgets.QFormLayout(Main)
        self.all_box.addRow(self.box_language_QRadioButton)
        self.all_box.addRow(self.box_word_QLabel)
        self.all_box.addRow(self.box_input_QLineEdit)
        self.all_box.addRow(self.box_button_QPushButton)
        self.all_box.setVerticalSpacing(30)

        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Dialog", "Admin"))
        # self.check_word.setText(_translate("Dialog", "Проверить"))


class Main(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.ongoing = False
        self.english_words = englishWords()
        self.english_words.create()
        self.count_el_db = len(self.english_words)
        self.sequence_of_words = [0]
        self.index_word = self.sequence_of_words[-1]
        self.answer = ""
        self.words = []
        self.setupUi(self)
        self.palette = self.palette()

        self.en_ru.toggled.connect(self._language)
        self.ru_en.toggled.connect(self._language)
        self.check_word.clicked.connect(self._verify)
        self.update_word.clicked.connect(self._new_word)

        self._language()

    def _language(self):
        self._update_window()
        if self.en_ru.isChecked():
            self.word2.show()
            self.word3.show()
            self.input2.hide()
            self.input3.hide()

        if self.ru_en.isChecked():
            self.word2.hide()
            self.word3.hide()
            self.input2.show()
            self.input3.show()

    def _verify(self):
        # self.click_one() if not self.ongoing else self.click_two()
        # self.ongoing = not self.ongoing
        if self.en_ru.isChecked():
            b = False
            for i in list(self.answer.split()):
                symbol = re.sub('[^a-zа-яё-]', '', i, flags=re.IGNORECASE)
                if self.input.text() == symbol or self.input.text() == symbol[:-2]:
                    b = True
                    break
            if b:
                self.input.setStyleSheet("background-color: #00e600")
                return
            if not self.ongoing:
                self.input.setStyleSheet("background-color: #990000")
            else:
                self.input.setText(self.answer)

        if self.ru_en.isChecked():
            if not self.ongoing:
                pass
            else:
                pass

        self.ongoing = not self.ongoing


    def _new_word(self):
        self._update_window()

        if self.en_ru.isChecked():
            self.sequence_of_words.append(self.random_Words())
            # print(self.sequence_of_words, self.sequence_of_words[-1])
            # print(self.english_words.get_db(self.sequence_of_words[-1]))
            self.words = self.english_words.get_db(self.sequence_of_words[-1])
            self.word.setText(self.words[0])
            self.word2.setText(self.words[1])
            self.word3.setText(self.words[2])
            self.answer = self.words[-1]
            pass

        if self.ru_en.isChecked():
            pass
        pass

    def _update_window(self):
        self.ongoing = False
        self.input.setStyleSheet("background-color: white")
        self.input.setText("")
        self.input2.setStyleSheet("background-color: white")
        self.input2.setText("")
        self.input3.setStyleSheet("background-color: white")
        self.input3.setText("")

        """ Будет изменять цвет фона приложения при правильном ответе   ( _verify  _new_word)"""
        # self.palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Window, QtGui.QColor("#4068a0"))
        # self.setPalette(self.palette)

    def random_Words(self,):
        rand = int(random.random() * self.count_el_db)
        while self.sequence_of_words[-1] == rand:
            rand = int(random.random() * self.count_el_db)
        return rand


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())
