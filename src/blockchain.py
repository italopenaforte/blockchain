import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests


class Blockchain:
    def __init__(self):
        self.chain = []  # stores all the chains of a blockchain
        self.current_transactions = []  # stores the transactions
        self.nodes = set()

        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,  # this is the index of a block
            "timestamp": time(),  # this is a timestamp when the block was created
            "transactions": self.current_transactions,  # the transactions that was performed
            "proof": proof,  # proof that this block is immutable
            "previous_hash": previous_hash
            or self.hash(self.chain[-1]),  # the hash of the last block created
        }

        self.current_transactions = []

        self.chain.append(block)

        return block

    def new_transction(self, sender, recipient, amount):
        # this is a simple transaction that is sending money to a person to another
        # that could be change to send chuncks of a file
        # or links from a page
        transaction = {
            "sender": sender,  # how is sender the amount
            "recipient": recipient,  # how is reciving the amout
            "amount": amount,  # the amount that is transaction
        }
        self.current_transactions.append(transaction)
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.startswith("0000")

    def register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        else:
            raise ValueError("Invalid URL")

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f"{last_block}")
            print(f"{block}")
            print("\n----------\n")

            if block["previous_hash"] != self.hash(last_block):
                return False

            if not self.valid_proof(last_block["proof"], block["proof"]):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f"http://{node}/chain")

            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False
