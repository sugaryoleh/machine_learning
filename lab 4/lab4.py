import sys
from io import StringIO
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import (QPushButton, QRadioButton, QPlainTextEdit)
import nltk
import random
from nltk.corpus import *
from nltk.book import text1, text2, text3, text4
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.init_UI()

    def init_UI(self):
        self.exec1_btn.clicked.connect(self.exec_task_1)
        self.exec2_btn.clicked.connect(self.exec_task_5)
        self.exec3_btn.clicked.connect(self.exec_task_7)
        self.exec4_btn.clicked.connect(self.exec_task_8)
        self.exec5_btn.clicked.connect(self.exec_task_9)
        self.exec6_btn.clicked.connect(self.exec_task_13)
        pass

    def exec_task_1(self):
        self.output.clear()
        self.output.appendPlainText(
            'Task #1 - Read "austen-persuasion.txt", display token count and unique word count:\n')

        words = gutenberg.words('austen-persuasion.txt')
        fd = FreqDist(words)

        self.output.appendPlainText('Token count: ' + str(len(words)))
        self.output.appendPlainText('Unique count: ' + str(len(fd.keys())))

        pass

    def exec_task_5(self):
        self.output.clear()
        self.output.appendPlainText(
            'Task #5 - Compare two texts\n')

        texts = text1, text2
        temp_out = StringIO()
        nltk.sys.stdout = temp_out

        for text in texts:
            fd = FreqDist(text)
            word_count = len(text)
            unique_count = len(fd.keys())
            temp_out.write(
                f"\nText:\t{text.name.title()};\n\tWord count: {word_count};\n\tUnique count: {unique_count};\n\tText richness {round(unique_count / word_count, 3)}%\nConcordance for word 'monstrous':\n\n")
            text.concordance("monstrous")

        self.output.appendPlainText(temp_out.getvalue())

        pass

    def exec_task_7(self):
        self.output.clear()
        self.output.appendPlainText('Task #7 - Words frequency >= 3:\n')

        fd = nltk.FreqDist(w.lower() for w in brown.words())
        words = [w for w in fd if fd[w] >= 3]
        for word in words:
            frequency = fd[word]
            self.output.appendPlainText(
                'Word: ' + word + ', freq.: ' + str(frequency))

        pass

    def exec_task_8(self):
        self.output.clear()
        self.output.appendPlainText(
            'Task #8 - Relation between total word count and unique word count in Brown genres:\n')

        for genreName in brown.categories():
            self.output.appendPlainText(genreName + ': ' + str(round(len(brown.words(categories=genreName)) /
                                                                     len(set(brown.words(categories=genreName))), 4)))
        pass

    def exec_task_9(self):
        self.output.clear()
        self.output.appendPlainText(
            'Task #9 - 50 most frequent words without meaningless ones in text "chats":\n')

        MIN_LENGTH = 5
        MIN_FREQ_DIST = 5
        chat_words = [w.lower() for w in nps_chat.words()]
        fd = nltk.FreqDist(chat_words)

        words = [w for w in set(chat_words) if fd[w] >
                 MIN_FREQ_DIST and len(w) > MIN_LENGTH and w.isalnum()]

        self.output.appendPlainText('; '.join(words[:50]))
        pass

    def exec_task_13(self):
        self.output.clear()
        self.output.appendPlainText(
            'Task #13 - Collocations for text #2 and #4\n\n')

        temp_out = StringIO()
        nltk.sys.stdout = temp_out

        temp_out.write('Text #2 collocations:\n')
        text2.collocations()
        temp_out.write('\nText #4 collocations:\n')
        text4.collocations()
        self.output.appendPlainText(temp_out.getvalue())

        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
