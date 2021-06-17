from flask import Flask, json, jsonify, request
from uuid import uuid4
from felipe_coin import Blockchain

app = Flask(__name__)
node_address = str(uuid4()).replace('-', '')
blockchain = Blockchain()

@app.route('/mine-block', methods=['GET'])
def mine_block():
  prev_block = blockchain.get_previous_block()
  prev_proof = prev_block['proof']
  proof = blockchain.proof_of_work(prev_proof)
  prev_hash = blockchain.hash(prev_block)
  blockchain.add_transaction(sender = node_address, receiver = 'Felipe', amount = 1)
  block = blockchain.create_block(proof, prev_hash)
  response = {
    'message': 'Congratulations, you just mined a block!',
    'index': block['index'],
    'timestamp': block['timestamp'],
    'proof': block['proof'],
    'prev_hash': block['prev_hash'],
    'transactions': block['transactions']
  }

  return jsonify(response), 200

@app.route('/get-chain', methods=['GET'])
def get_chain():
  response = { 'chain': blockchain.chain, 'length': len(blockchain.chain) }
  return jsonify(response), 200

@app.route('/is-valid', methods=['GET'])
def is_valid():
  is_valid = blockchain.is_chain_valid(blockchain.chain)

  if is_valid:
    response = {'message': 'Chain is valid', 'result': True}
  else:
    response = {'message': "Chain is invalid", 'result': False}
    
  return jsonify(response), 200

@app.route('/add-transaction', methods=['POST'])
def add_transaction():
  json = request.get_json()
  transaction_keys = ['sender', 'receiver', 'amount']

  if not all (key in json for key in transaction_keys):
    return 'elements missing', 400

  index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
  response = {'message': f'transaction added to block {index}'}

  return jsonify(response), 201

app.run(host = '0.0.0.0', port = 5000)