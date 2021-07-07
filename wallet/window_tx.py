from PyQt5.QtWidgets import QDialog

from wallet.gui_about import Ui_Dialog


class TXWindow(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)