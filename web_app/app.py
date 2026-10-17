import os
import httpx
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'development-only-key')
API_GATEWAY_URL = 'http://localhost:8000'
TIMEOUT = 5.0


@app.route('/')
def index():
    return render_template('index.html')


def fetch_list(path):
    response = httpx.get(f'{API_GATEWAY_URL}/{path}', timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


@app.route('/products')
def products():
    try:
        data = fetch_list('products')
    except httpx.HTTPError as exc:
        flash(f'Ошибка загрузки товаров: {exc}', 'error')
        data = []
    return render_template('products.html', products=data)


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        try:
            order_data = {
                'product_id': int(request.form['product_id']),
                'customer_id': int(request.form['customer_id']),
                'quantity': int(request.form['quantity']),
            }
            if any(value < 1 for value in order_data.values()):
                raise ValueError('Значения должны быть положительными')
            response = httpx.post(f'{API_GATEWAY_URL}/orders', json=order_data, timeout=TIMEOUT)
            response.raise_for_status()
            flash('Заказ успешно создан!', 'success')
            return redirect(url_for('orders'))
        except (httpx.HTTPError, ValueError, KeyError) as exc:
            flash(f'Ошибка создания заказа: {exc}', 'error')
    try:
        data = fetch_list('orders')
    except httpx.HTTPError as exc:
        flash(f'Ошибка загрузки заказов: {exc}', 'error')
        data = []
    return render_template('orders.html', orders=data)


@app.route('/customers')
def customers():
    try:
        data = fetch_list('customers')
    except httpx.HTTPError as exc:
        flash(f'Ошибка загрузки клиентов: {exc}', 'error')
        data = []
    return render_template('customers.html', customers=data)


if __name__ == '__main__':
    app.run(port=5004, debug=True)
