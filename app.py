from flask import Flask, jsonify
from google_sheets_integration import get_inventory

app = Flask(__name__)

@app.route('/get-inventory', methods=['GET'])
def inventory():
    inventory_data = get_inventory()
    return jsonify(inventory_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
