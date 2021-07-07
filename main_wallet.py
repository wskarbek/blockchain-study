import sys

from PyQt5.QtWidgets import QApplication

from wallet.window_wallet import WindowMain

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowMain()
    win.show()
    sys.exit(app.exec())
