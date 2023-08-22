from PyQt6 import QtWidgets

from ui.generated.about import Ui_Dialog


class AboutDialog(QtWidgets.QDialog, Ui_Dialog):
    """A simple about screen just to show who made this"""
    def __init__(self, *args, **kwargs) -> None:
        super(AboutDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.action_close_button)

    def action_close_button(self) -> None:
        """Close the window when clicking the close button"""
        self.close()
