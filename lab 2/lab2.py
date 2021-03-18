import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QLabel, QTableWidget,
                             QTableWidgetItem)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QToolTip, QPushButton, QMessageBox)
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.utils import Bunch
from PyQt5.QtCore import QAbstractTableModel, Qt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from matplotlib import pyplot as plt

# клас моделі DataFrame для вивиоду у QTableView


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.init_UI()

    def init_UI(self):
        self.exec_btn.clicked.connect(self.execute_task)
        pass

    def execute_task(self):
        self.task_output.clear()
        pd.set_option('display.float_format', lambda x: '{: 6.2f}'.format(x))
        cancer = load_breast_cancer()

        # виводимо загальну інформацію про датасет
        self.gen_desc.setText(cancer.DESCR)

        # виводимо перші 5 рядків датасету
        self.print_dataset_rows(cancer, 5)

        # Розбиваємо датасет на навчальну та тестову вибірки
        X_train, X_test, y_train, y_test = train_test_split(
            cancer.data, cancer.target, stratify=cancer.target, random_state=42)

        # Виводимо опис характеристик ознак
        df_test = pd.DataFrame(X_test)
        self.task_output.appendPlainText(
            "Descriptive statistics:\n\n" + df_test.describe().to_string())

        # Два списки для збереження точності для різних налаштування кількості сусідів
        training_accuracy = []
        test_accuracy = []

        k_from = int(self.k_from.value())
        k_to = int(self.k_to.value())

        if k_from > k_to:
            self.print_error('Invalid k range!')
            return

        # Налаштування інтервалу кількості сусідів
        neighbors_settings = range(k_from, k_to + 1)

        # виконуємо обчислення для всього інтервалу
        for n_neighbors in neighbors_settings:
            # створюємо класифікатор KNN
            clf = KNeighborsClassifier(n_neighbors=n_neighbors)
            clf.fit(X_train, y_train)

            # записуємо точності для тестової та навчальної вибірок
            training_accuracy.append(clf.score(X_train, y_train))
            test_accuracy.append(clf.score(X_test, y_test))
            prediction = clf.predict(X_test)

        # Вивід графіку співвідношення кількості сусідів до точності
        plt.plot(neighbors_settings, training_accuracy,
                 label='Accuracy of the Training Set')
        plt.plot(neighbors_settings, test_accuracy,
                 label='Accuracy of the Test Set')
        plt.ylabel('Accuracy')
        plt.xlabel('Number of Neighbors')
        plt.legend()
        plt.title("KNN - Accuracy score")
        plt.show()

        pass

    def print_dataset_rows(self, cancer, count):
        df = pd.DataFrame(np.c_[cancer['data'], cancer['target']], columns=np.append(
            cancer['feature_names'], ['target']))

        model = PandasModel(df.head(n=count))
        self.stats_view.setModel(model)
        pass

    def print_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
