import json
import pickle
import sys
import hashlib
from collections import OrderedDict

from hash_tools import hash_string, hash_block
from block import Block
from transaction import Transaction

MINING_REWARD = 10
OWNER = "Jesx"

blockchain = []
open_transactions = []


def save_data():
    try:
        with open('puch.blockchain', mode='w') as f:
            f.write(json.dumps([block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.txs], block_el.proof, block_el.timestamp) for block_el in blockchain]]))
            f.write('\n')
            f.write(json.dumps([tx.__dict__ for tx in open_transactions]))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving failed!')


def load_data():
    global blockchain
    global open_transactions
    try:
        with open('puch.blockchain', mode='r') as f:
            # file_content = pickle.loads(f.read())
            file_content = f.readlines()

            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['txs']]
                updated_block = Block(
                    block['index'],
                    block['previous_hash'],
                    converted_tx,
                    block['proof'],
                    block['timestamp']
                )

                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_open_txs = []
            for tx in open_transactions:
                updated_open_tx = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_open_txs.append(updated_open_tx)
            open_transactions = updated_open_txs
    except IOError:
        genesis_block = Block(0, 'GENESIS', [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.txs if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx.amount for tx in block.txs if tx.recipient == participant] for block in
                    blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


def add_transaction(sender, recipient, date, amount):
    transaction = Transaction(sender, recipient, amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def valid_proof(txs, last_hash, proof):
    guess = (str([tx.to_ordered_dict() for tx in txs]) + str(last_hash) + str(proof)).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[0:2] == 'ff'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = Transaction('GENESIS', OWNER, MINING_REWARD)
    open_tx_copy = open_transactions[:]
    open_tx_copy.append(reward_transaction)
    block = Block(
        len(blockchain),
        hashed_block,
        open_tx_copy,
        proof
    )
    print(block)
    print('-' * 197)
    blockchain.append(block)
    open_transactions.clear()
    save_data()


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.txs[:-1], block.previous_hash, block.proof):
            print('PoW is invalid')
            return False
    return True


def verify_txs():
    return all([verify_transaction(tx) for tx in open_transactions])


def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount


load_data()
add_transaction("Jesx", "A", 0, 21.372137)
mine_block()
add_transaction("Jesx", "B", 0, 15.158475)
mine_block()
print("VERIFY: " + str(verify_chain()))
print("JESX: ", get_balance("Jesx"), "PUCH")
print("A:", get_balance("A"), "PUCH")
print("B:", get_balance("B"), "PUCH")
print(verify_txs())
