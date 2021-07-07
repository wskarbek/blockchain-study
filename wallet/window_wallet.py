import requests
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from wallet.gui_wallet import Ui_MainWindow
from wallet.window_about import AboutWindow
from wallet.window_tx import TXWindow
from puchchain.wallet import Wallet


class WindowMain(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signal_slots()
        self.about_window = AboutWindow()
        self.tx_window = TXWindow()
        self.wallet = Wallet()
        self.network = "wskarbek.xyz:7000"
        self.balance = 0

    def get_and_set_balance(self):
        res = requests.get('http://{}/balance/{}'.format(self.network, self.wallet.public_key))
        self.balance = res.json()['funds']
        self.lineEditBalance.setText("{} PUCH".format(self.balance))

    def set_address(self):
        self.lineEditPublicKey.setText(str(self.wallet.public_key))

    def create_wallet_and_save_to_file(self):
        self.wallet.create_keys()
        file_path = QFileDialog.getSaveFileName(self, 'Save wallet', filter="Wallet File (*.dat)")
        if file_path[0] != '':
            self.wallet.save_keys(file_path)

    def load_wallet_from_file(self):
        file_path = QFileDialog.getOpenFileName(self, 'Load wallet', filter="Wallet File (*.dat)")
        if file_path[0] != '':
            self.wallet.load_keys(file_path)
        if self.wallet.public_key is not None:
            self.get_and_set_balance()
            self.set_address()

    def connect_signal_slots(self):
        self.actionAbout_Puch.triggered.connect(self.about)
        self.actionCreate_wallet.triggered.connect(lambda: self.create_wallet_and_save_to_file())
        self.actionLoad_wallet.triggered.connect(lambda: self.load_wallet_from_file())
        self.pushButton_2.clicked.connect(lambda: self.get_and_set_balance())

    def about(self):
        self.about_window.show()
