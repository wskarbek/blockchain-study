from time import time


class Block:
    def __init__(self, index, previous_hash, txs, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time
        self.txs = txs
        self.proof = proof

    def __repr__(self):
        return 'BLOCK: {}, HASH: {}, PROOF: {}, TXS: {}'.format(self.index, self.previous_hash, self.proof, self.txs)
