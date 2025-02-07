from flask import Flask, request, jsonify, render_template
import json
import os
from blockchain import Blockchain

app = Flask(__name__, template_folder="templates", static_folder="static")
blockchain = Blockchain()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()
    blockchain.add_transaction(data["sender"], data["receiver"], data["product"], data["quantity"], data["price"])
    return jsonify({"message": "Transaction added successfully!"}), 201

@app.route("/mine", methods=["GET"])
def mine_block():
    previous_block = blockchain.chain[-1]
    new_block = blockchain.create_block(previous_block["hash"])
    return jsonify({"message": "Block Mined!", "block": new_block}), 200

@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify({"chain": blockchain.get_chain()}), 200

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "" or not file.filename.endswith(".json"):
        return jsonify({"message": "Invalid file format"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    with open(filepath, "r") as f:
        transactions = json.load(f)
        for transaction in transactions:
            blockchain.add_transaction(transaction["sender"], transaction["receiver"], transaction["product"], transaction["quantity"], transaction["price"])
    
    return jsonify({"message": "Transactions added from file!"}), 201

if __name__ == "__main__":
    app.run(debug=True)
