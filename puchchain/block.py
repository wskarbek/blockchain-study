from time import time


class Block:
    def __init__(self, index, previous_hash, txs, stake_txs, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time
        self.txs = txs
        self.stake_txs = stake_txs
        self.proof = proof

    def __repr__(self):
        return 'BLOCK: {}, HASH: {}, PROOF: {}, TXS: {}, STAKE_TXS: {}'\
            .format(self.index, self.previous_hash, self.proof, self.txs, self.stake_txs)
