from flask import Flask, jsonify

app = Flask(__name__)
customers = [
    {"id": 1, "name": "Customer A"},
    {"id": 2, "name": "Customer B"},
    {"id": 3, "name": "Customer C"},
]


@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers)


@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = next((c for c in customers if c['id'] == customer_id), None)
    return jsonify(customer) if customer else ('Not Found', 404)


if __name__ == '__main__':
    app.run(port=5003, debug=True)
