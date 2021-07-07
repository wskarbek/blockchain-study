from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from puchchain.wallet import Wallet
from puchchain.blockchain import Blockchain

app = Flask(__name__)
CORS(app)


# API Stuff
@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        res = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(res), 200
    else:
        res = {
            'message': 'Saving the wallet keys failed.'
        }
        return jsonify(res), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        res = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(res), 200
    else:
        res = {
            'message': 'Loading wallet keys failed.'
        }
        return jsonify(res), 500


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = [block.__dict__.copy() for block in blockchain.chain]
    for chain_block in chain:
        chain_block['txs'] = [tx.__dict__ for tx in chain_block['txs']]
    return jsonify(chain), 200


# To be removed, old TX sending
# @app.route('/transactions', methods=['GET'])
# def get_open_tx():
#     txs = blockchain.get_open_txs()
#     dict_transactions = [tx.__dict__ for tx in txs]
#     return jsonify(dict_transactions), 200
#     res = {
#         'message': 'Fetched transactions successfully.',
#         'ttransactions': dict_transactions
#     }


# Wallet related stuff
@app.route('/balance/<account>', methods=['GET'])
def get_balance(account):
    balance = blockchain.get_balance(account)
    if balance is not None:
        res = {
            'message': 'Successfully fetched balance.',
            'funds': blockchain.get_balance()
        }
        return jsonify(res), 201
    else:
        res = {
            'message': 'Loading balance failed.',
            'wallet': wallet.public_key
        }
        return jsonify(res), 500


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key is None:
        res = {
            'message': 'No wallet.'
        }
        return jsonify(res), 400
    values = request.get_json()
    if not values:
        res = {
            'message': 'No json data received.'
        }
        return jsonify(res), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        res = {
            'message': 'Required data is missing.'
        }
        return jsonify(res), 400
    amount = values['amount']
    recipient = values['recipient']
    signature = wallet.sign_tx(wallet.public_key, values['recipient'], values['amount'])
    tx_success = blockchain.add_transaction(wallet.public_key, values['recipient'], signature, amount=values['amount'])
    if tx_success:
        res = {
            'message': 'Successfully added transaction.',
            'tx': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(res), 201
    else:
        res = {
            'message': 'Creating a transaction failed.'
        }
        return jsonify(res), 500


# TODO: Replace with PoS
@app.route('/mine', methods=['POST'])
def mine():
    if blockchain.resolve_conflicts:
        res = {
            'message': 'Resolve conflicts first, block not added!'
        }
        return jsonify(res), 409
    block = blockchain.mine_block()
    if block is not None:
        block = block.__dict__.copy()
        block['txs'] = [tx.__dict__ for tx in block['txs']]
        res = {
            'message': 'Block mined.',
            'block': block,
            'funds': blockchain.get_balance()
        }
        return jsonify(res), 201
    else:
        res = {
            'message': 'Adding a block failed.',
            'wallet': wallet.public_key
        }
        return jsonify(res), 500


# Consensus related stuff
@app.route('/resolve-conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        res = {
            'message': 'Chain was replaced!'
        }
    else:
        res = {
            'message': 'Chain up to date'
        }
    return jsonify(res), 200


@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        res = {
            'message': 'No data found.'
        }
        return jsonify(res), 400
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(key in values for key in required):
        res = {
            'message': 'Some data is missing.'
        }
        return jsonify(res), 400
    success = blockchain.add_transaction(values['sender'], values['recipient'], values['signature'], values['amount'],
                                         is_receiving=True)
    if success:
        res = {
            'message': 'Successfully added transaction.',
            'tx': {
                'sender': values['sender'],
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': values['signature']
            }
        }
        return jsonify(res), 201
    else:
        res = {
            'message': 'Creating a transaction failed.'
        }
        return jsonify(res), 500


@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        res = {
            'message': 'No data found.'
        }
        return jsonify(res), 400
    if 'block' not in values:
        res = {
            'message': 'Block data is missing.'
        }
        return jsonify(res), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            res = {
                'message': 'Block added'
            }
            return jsonify(res), 200
        else:
            res = {
                'message': 'Block seems invalid.'
            }
            return jsonify(res), 409
    elif block['index'] > blockchain.chain[-1].index:
        res = {
            'message': 'Blockchain seems to differ from local blockchain.'
        }
        blockchain.resolve_conflicts = True
        return jsonify(res), 200
    else:
        res = {
            'message': 'Blockchain seems to be shorter, block not added'
        }
        return jsonify(res), 409


# Node related stuff
@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        res = {
            'message': 'No data received.'
        }
        return jsonify(res), 400
    if not "node" in values:
        res = {
            'message': 'No node data found.'
        }
        return jsonify(res), 400
    node = values['node']
    blockchain.add_peer_node(node)
    res = {
        'message': 'Node added successfully.',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(res), 201


@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url is None:
        res = {
            'message': 'No node data found.'
        }
        return jsonify(res), 400
    blockchain.remove_peer_node(node_url)
    res = {
        'message': 'Node removed',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(res), 200


@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    res = {
        'all_nodes': nodes
    }
    return jsonify(res), 200


def run_server():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host="0.0.0.0", port=port)

