import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transactions,
            'previous_hash': previous_hash,
            'hash': self.hash_block(self.transactions, previous_hash)
        }
        self.transactions = []
        self.chain.append(block)
        return block
    
    def hash_block(self, transactions, previous_hash):
        encoded_block = json.dumps(transactions, sort_keys=True).encode()
        return hashlib.sha256(encoded_block + previous_hash.encode()).hexdigest()
    
    def add_transaction(self, sender, receiver, product, quantity, price):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'product': product,
            'quantity': quantity,
            'price': price
        })
        return len(self.chain) + 1

    def get_chain(self):
        return self.chain
