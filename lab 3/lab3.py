import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import (QRadioButton, QComboBox, QSpinBox, QPushButton)
import matplotlib.pyplot as plot
import numpy as np
import mglearn
import sklearn.datasets
from sklearn.datasets import load_breast_cancer


class Window(QtWidgets.QMainWindow):
    markers = {'point': '.', 'pixel': ',', 'circle': 'o', 'octagon': '8', 'square': 's',
               'triangle_down': 'v', 'triangle_up': '^', 'star': '*', 'plus_filled': 'P', 'none': ''}

    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.init_UI()

    def init_UI(self):
        self.show_plot.clicked.connect(self.exec_show_plot)
        self.show_histogram.clicked.connect(self.exec_show_histogram)
        pass

    def exec_show_plot(self):
        label = 'Y(x) = cos(x ^ 2) / x'
        line_color = self.lineColor.currentText()
        line_style = self.lineStyle.currentText()
        line_width = self.lineWidth.value()
        marker_count = self.markerCount.value()
        marker_color = self.markerColor.currentText()
        marker_style = self.markerStyle.currentText()

        x = np.linspace(1, 10, marker_count)
        y = np.cos(x * x) / x

        plot.plot(x, y, label=label, color=line_color, markerfacecolor=marker_color, markeredgecolor=marker_color,
                  marker=self.markers[marker_style], linestyle=line_style, linewidth=line_width)
        plot.legend([label], loc='upper right')
        plot.xlabel('x')
        plot.ylabel('y')
        plot.title('Graph: ' + label)
        plot.savefig('graph.png')
        plot.show()

    def exec_show_histogram(self):
        cancer = load_breast_cancer()
        fig, axes = plot.subplots(10, 3, figsize=(10, 20))
        malignant = cancer.data[cancer.target == 0]
        benign = cancer.data[cancer.target == 1]

        axe = axes.ravel()
        color = self.labels_color.currentText()

        for i in range(30):
            _, bins = np.histogram(cancer.data[:, i], bins=50)
            axe[i].hist(malignant[:, i], bins=bins,
                        color=mglearn.cm3(0), alpha=.5)
            axe[i].hist(benign[:, i], bins=bins,
                        color=mglearn.cm3(2), alpha=.5)
            axe[i].set_title(cancer.feature_names[i], color=color)
            axe[i].set_yticks(())
            plot.tick_params(axis='x', colors=color)
            plot.tick_params(axis='y', colors=color)
            axe[i].set_xlabel("Feature magnitude", color=color)
            axe[i].set_ylabel("Frequency", color=color)
            axe[i].legend(cancer.target_names, loc="best")

        fig.tight_layout()
        plot.savefig('histogram.png')
        plot.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
