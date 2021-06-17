import datetime
import hashlib
import json
import requests
from urllib import urlparse


class Blockchain:
  def __init__(self):
    self.chain = []
    self.pendingTransactions = []
    self.create_block(proof = 1, prev_hash = '0')
    self.nodes = set()

  def create_block(self, proof, prev_hash):
    block = {
      'index': len(self.chain) + 1,
      'timestamp': str(datetime.datetime.now()),
      'proof': proof,
      'prev_hash': prev_hash,
      'transactions': self.pendingTransactions
    }

    self.pendingTransactions = []
    self.chain.append(block)
    return block

  def get_previous_block(self):
    return self.chain[-1]

  def proof_of_work(self, prev_proof):
    new_proof = 1
    check_proof = False

    while check_proof is False:
      hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()

      if hash_operation[:4] == '0000':
        check_proof = True
      else:
        new_proof += 1
      
    return new_proof

  def hash(self, block):
    encoded_block = json.dumps(block, sort_keys = True).encode()
    return hashlib.sha256(encoded_block).hexdigest()

  def is_chain_valid(self, chain):
    prev_block = chain[0]
    block_index = 1

    while block_index < len(chain):
      block = chain[block_index]

      if block['prev_hash'] != self.hash(prev_block):
        return False  

      prev_proof = prev_block['proof']
      proof = block['proof']
      hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()

      if hash_operation[:4] != '0000':
        return False

      prev_block = block
      block_index += 1

    return True

  def add_transaction(self, sender, receiver, amount):
    self.pendingTransactions.append({ 'sender': sender, 'receiver': receiver, 'amount': amount })
    prev_block = self.get_previous_block()
    return prev_block['index'] + 1

  def add_node(self, address):
    parsed_url = urlparse(address)
    self.nodes.add(parsed_url.netloc)

  def replace_chain(self):
    network = self.nodes
    longest_chain = None
    max_len = len(self.chain)

    for node in network:
      response = requests.get(f'http://{node}/get_chain')
      if response.status_code == 200:
        chain_len = response.json()['length']
        chain = response.json()['chain']

        if chain_len > max_len and self.is_chain_valid(chain):
          longest_chain = chain
          max_len = chain_len

    if longest_chain:
      self.chain = longest_chain  
      return True
    
    return False