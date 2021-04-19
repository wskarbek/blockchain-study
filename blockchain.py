import json

from block import Block
from transaction import Transaction
from wallet import Wallet

from util.verification import Verification
from util.hash_tools import hash_block

MINING_REWARD = 10


class Blockchain:
    def __init__(self, user):
        genesis_block = Block(0, 'GENESIS', [], 100, 0)
        self.chain = [genesis_block]
        self.open_transactions = []
        self.verifier = Verification()
        self.user = user
        # self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def save_data(self):
        try:
            with open('puch.blockchain', mode='w') as f:
                f.write(json.dumps([block.__dict__ for block in [
                    Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.txs], block_el.proof,
                          block_el.timestamp) for block_el in self.chain]]))
                f.write('\n')
                f.write(json.dumps([tx.__dict__ for tx in self.open_transactions]))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')

    def load_data(self):
        try:
            with open('puch.blockchain', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()

                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']

                self.chain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in self.chain:
                    converted_tx = [Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['signature'],
                        tx['amount']
                    ) for tx in block['txs']]
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_tx,
                        block['proof'],
                        block['timestamp']
                    )

                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_open_txs = []
                for tx in open_transactions:
                    updated_open_tx = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_open_txs.append(updated_open_tx)
                self.open_transactions = updated_open_txs
        except IOError:
            genesis_block = Block(0, 'GENESIS', [], 100, 0)
            self.chain = [genesis_block]
            self.open_transactions = []

    def get_balance(self, participant):
        tx_sender = [[tx.amount for tx in block.txs if tx.sender == participant] for block in self.chain]
        open_tx_sender = [tx.amount for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = 0
        for tx in tx_sender:
            if len(tx) > 0:
                amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in block.txs if tx.recipient == participant] for block in
                        self.chain]
        amount_received = 0
        for tx in tx_recipient:
            if len(tx) > 0:
                amount_received += tx[0]
        return amount_received - amount_sent

    def add_transaction(self, sender, recipient, signature, date, amount):
        if self.user is None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_tx(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not self.verifier.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def mine_block(self):
        if self.user is None:
            return False
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('GENESIS', self.user, '', MINING_REWARD)
        open_tx_copy = self.open_transactions[:]
        for tx in self.open_transactions:
            if not Wallet.verify_tx(tx):
                return False
        open_tx_copy.append(reward_transaction)
        block = Block(
            len(self.chain),
            hashed_block,
            open_tx_copy,
            proof
        )
        print(block)
        print('-' * 197)
        self.__chain.append(block)
        self.open_transactions.clear()
        self.save_data()
