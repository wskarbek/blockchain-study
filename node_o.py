from blockchain import Blockchain
from util.verification import Verification
from wallet import Wallet

verifier = Verification()


class Node:
    def __init__(self):
        self.wallet = Wallet()
        self.blockchain = None

    def run_chain(self):
        # self.wallet.create_keys()
        # self.wallet.save_keys()
        self.wallet.load_keys()
        self.blockchain = Blockchain(self.wallet.public_key)
        print(self.wallet.private_key)
        print(self.wallet.public_key)
        blockchain = Blockchain(self.wallet.public_key)
        blockchain.load_data()
        blockchain.mine_block()
        blockchain.add_transaction(self.wallet.public_key, "JESX", self.wallet.sign_tx(self.wallet.public_key, "JESX", 10), "JESX", 10)
        print(self.wallet.public_key, ": ", blockchain.get_balance(), "PUCH")
        print("JESX:", blockchain.get_balance(), "PUCH")
        # blockchain = Blockchain()
        # blockchain.load_data()
        # blockchain.mine_block()
        # blockchain.mine_block()
        # blockchain.mine_block()
        # blockchain.mine_block()
        # blockchain.add_transaction("Jesx", "A", 0, 21.372137)
        # blockchain.mine_block()
        # blockchain.add_transaction("Jesx", "B", 0, 15.158475)
        # blockchain.mine_block()
        #
        print("VERIFY: " + str(verifier.verify_chain(blockchain.chain)))
        # print("JESX: ", blockchain.get_balance("Jesx"), "PUCH")
        # print("A:", blockchain.get_balance("A"), "PUCH")
        # print("B:", blockchain.get_balance("B"), "PUCH")
        print(verifier.verify_txs(blockchain.open_transactions, blockchain.get_balance))
