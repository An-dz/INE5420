from PyQt6 import QtWidgets

from .generated.about import Ui_Dialog


class AboutDialog(QtWidgets.QDialog, Ui_Dialog):
    """docstring for AboutDialog"""
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.actionCloseButton)

    def actionCloseButton(self):
        self.close()
