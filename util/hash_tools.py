import hashlib
import json


def hash_string(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """Hashes a block and returns the hash.

    Arguments:
        :block: The block that will be hashed.
    """
    hashable_block = block.__dict__.copy()
    hashable_block['txs'] = [tx.to_ordered_dict() for tx in hashable_block['txs']]
    return hash_string(json.dumps(hashable_block, sort_keys=True).encode())
