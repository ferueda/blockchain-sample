from flask import Flask, json, jsonify
from werkzeug.wrappers import response
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine-block', methods=['GET'])
def mine_block():
  prev_block = blockchain.get_previous_block()
  prev_proof = prev_block['proof']
  proof = blockchain.proof_of_work(prev_proof)
  prev_hash = blockchain.hash(prev_block)
  block = blockchain.create_block(proof, prev_hash)
  response = {
    'message': 'Congratulations, you just mined a block!',
    'index': block['index'],
    'timestamp': block['timestamp'],
    'proof': block['proof'],
    'prev_hash': block['prev_hash']
  }

  return jsonify(response), 200




