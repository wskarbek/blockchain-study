import sys
import hashlib
import json

genesis_block = {
        'index': 0,
        'previous_block_hash': 'GENESIS',
        'transactions': []
}
blockchain = [genesis_block]
open_transactions = []

def add_transaction(sender, recipient, date, amount):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'date': date,
        'amount': amount
    }
    open_transactions.append(transaction)

def hash_block(block):
    hashed_block = '-'.join([str(block[key]) for key in block])
    #s.update(hashed_block.encode("utf-8"))
    #return s.hexdigest()
    return hashlib.sha256(json.dumps(block).encode()).hexdigest()

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    block = {
        'index': len(blockchain),
        'previous_block_hash': hashed_block,
        'transactions': open_transactions.copy()
    }
    print("NEW BLOCK #" + str(len(blockchain)) + "\n" + str(block))
    print('-' * 197)
    blockchain.append(block)
    open_transactions.clear()

def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_block_hash'] != hash_block(blockchain[index-1]):
            return False
    return True

add_transaction("A", "B", 0, 2.0)
mine_block()
add_transaction("A", "C", 0, 21.37)
mine_block()
add_transaction("B", "C", 0, 15.0)
mine_block()
print("VERIFY: " + str(verify_chain()))