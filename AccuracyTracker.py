import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt
import pandas as pd


class TrackerWindow(QWidget):
    def __init__(self, reset_count=65):
        super().__init__()
        self.initUI()
        self.df = pd.read_csv('data.csv')
        self.reset_count = reset_count

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Easy_counter')
        self.setGeometry(100, 100, 400, 150)

        self.correct_counter = 0
        self.incorrect_counter = 0

        self.correct_label = QLabel('Correct', self)
        self.correct_label.setGeometry(80, 10, 50, 30)
        self.correct_counter_label = QLabel(str(self.correct_counter), self)
        self.correct_counter_label.setGeometry(95, 50, 50, 30)

        self.incorrect_label = QLabel('Incorrect', self)
        self.incorrect_label.setGeometry(275, 10, 50, 30)
        self.incorrect_counter_label = QLabel(str(self.incorrect_counter), self)
        self.incorrect_counter_label.setGeometry(295, 50, 50, 30)

        self.correct_plus_button = QPushButton('+', self)
        self.correct_plus_button.setGeometry(55, 90, 30, 30)
        self.correct_plus_button.clicked.connect(self.incrementCorrectCounter)

        self.correct_minus_button = QPushButton('-', self)
        self.correct_minus_button.setGeometry(115, 90, 30, 30)
        self.correct_minus_button.clicked.connect(self.decrementCorrectCounter)

        self.incorrect_plus_button = QPushButton('+', self)
        self.incorrect_plus_button.setGeometry(255, 90, 30, 30)
        self.incorrect_plus_button.clicked.connect(self.incrementIncorrectCounter)

        self.incorrect_minus_button = QPushButton('-', self)
        self.incorrect_minus_button.setGeometry(315, 90, 30, 30)
        self.incorrect_minus_button.clicked.connect(self.decrementIncorrectCounter)

        self.show()

    def incrementCorrectCounter(self):
        self.correct_counter += 1
        self.updateCounterLabel()

    def decrementCorrectCounter(self):
        if self.correct_counter > 0:
            self.correct_counter -= 1
        self.updateCounterLabel()

    def incrementIncorrectCounter(self):
        self.incorrect_counter += 1
        self.updateCounterLabel()

    def decrementIncorrectCounter(self):
        if self.incorrect_counter > 0:
            self.incorrect_counter -= 1
        self.updateCounterLabel()

    def updateCounterLabel(self):
        self.correct_counter_label.setText(str(self.correct_counter))
        self.incorrect_counter_label.setText(str(self.incorrect_counter))

        if self.correct_counter + self.incorrect_counter == self.reset_count:
            self.saveAndResetCounter()

    def saveAndResetCounter(self):
        new_data = {'Correct': str(self.correct_counter), 'Incorrect': str(self.incorrect_counter), 
                    'Accuracy': round(self.correct_counter / (self.correct_counter + self.incorrect_counter), 2)}
        self.df = pd.concat([self.df, pd.DataFrame(new_data, index=[0])], ignore_index=True)
        self.df.to_csv('data.csv', index=False)
        self.correct_counter = 0
        self.incorrect_counter = 0
        self.updateCounterLabel()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_U:
            self.incrementCorrectCounter()
        elif key == Qt.Key_I:
            self.decrementCorrectCounter()
        elif key == Qt.Key_O:
            self.incrementIncorrectCounter()
        elif key == Qt.Key_P:
            self.decrementIncorrectCounter()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TrackerWindow()
    sys.exit(app.exec_())
