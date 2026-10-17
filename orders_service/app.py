from flask import Flask, jsonify, request

app = Flask(__name__)
orders = []


@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)


@app.route('/orders', methods=['POST'])
def create_order():
    order = request.get_json()
    order['id'] = len(orders) + 1
    orders.append(order)
    return jsonify(order), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)
