genesis_block = {
        'previous_block_hash': 'GENESIS',
        'index': 0,
        'transactions': []
}
blockchain = [genesis_block]
open_transactions = []

def get_last_blockchain_value():
    """Returns the last value of the current blockchain."""
    if len(blockchain) < 1:
        return none
    return blockchain[-1]

def add_transaction(sender, recipient, amount):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    open_transactions.append(transaction)

def hash_block(last_block):
    hashed_block = str(last_block["index"]) + "-" + str(last_block["previous_block_hash"]) + "-"
    for transaction in last_block["transactions"]:
        hashed_block = hashed_block + "\n" + str(transaction) 
    return hashed_block


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    print("PREV BLOCK\n" + hashed_block + "\n")
    block = {
        'index': len(blockchain),
        'previous_block_hash': last_block,
        'transactions': open_transactions
    }
    print("NEW BLOCK #" + str(len(blockchain)) + "\n" + str(block) + "\n")
    print('-' * 197)
    open_transactions.clear()
    blockchain.append(block)

def verify_chain():
    i = 0
    valid = True
    for block in blockchain:
        if i == 0:
            i+=1
            continue
        elif block[0] == blockchain[i - 1]:
            valid = True
        else:
            valid = False
            break
        i+=1
    return valid

add_transaction("A", "B", 2.0)
mine_block()
add_transaction("A", "B", 15.0)
add_transaction("A", "C", 6.0)
mine_block()
add_transaction("A", "D", 3.0)
mine_block()