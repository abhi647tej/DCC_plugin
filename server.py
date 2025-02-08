from flask import Flask, request, jsonify
import time
import sqlite3

app = Flask(__name__)

# Simulate 10-second delay  
def delayed_response(data):
    time.sleep(10)
    return jsonify(data)

@app.before_request
def log_request():
    print(f"Received {request.method} request at {request.path}")

# Define API Endpoints
@app.route('/transform', methods=['POST'])
def transform():
    data = request.json
    return delayed_response({"message": "Transform received", "data": data})

@app.route('/translation', methods=['POST'])
def translation():
    data = request.json
    return delayed_response({"message": "Translation received", "data": data})

@app.route('/rotation', methods=['POST'])
def rotation():
    data = request.json
    return delayed_response({"message": "Rotation received", "data": data})

@app.route('/scale', methods=['POST'])
def scale():
    data = request.json
    return delayed_response({"message": "Scale received", "data": data})

@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.json
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (data["name"], data["quantity"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item added"})

@app.route('/remove-item', methods=['POST'])
def remove_item():
    data = request.json
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE name=?", (data["name"],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item removed"})

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    data = request.json
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET quantity=? WHERE name=?", (data["quantity"], data["name"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Quantity updated"})

@app.route('/get-inventory', methods=['GET'])
def get_inventory():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = [{"name": row[0], "quantity": row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify({"inventory": items})
      

if __name__ == '__main__':
    app.run(debug=True)
