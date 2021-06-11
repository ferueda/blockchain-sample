import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
  def __init__(self):
    self.chain = []
    self.create_block(proof = 1, prev_hash = '0')

  def create_block(self, proof, prev_hash):
    block = {
      'index': len(self.chain) + 1,
      'timestamp': str(datetime.datetime.now()),
      'proof': proof,
      'prev_hash': prev_hash,
    }

    self.chain.append(block)
    return block