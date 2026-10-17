from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title='API Gateway', version='1.0.0')
PRODUCTS_SERVICE = 'http://localhost:5001'
ORDERS_SERVICE = 'http://localhost:5002'
CUSTOMERS_SERVICE = 'http://localhost:5003'
TIMEOUT = 5.0


async def proxy(method, url, payload=None):
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.request(method, url, json=payload)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail='Not found')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f'Service unavailable: {exc}') from exc


@app.get('/products')
async def get_products():
    return await proxy('GET', f'{PRODUCTS_SERVICE}/products')


@app.get('/products/{product_id}')
async def get_product(product_id: int):
    return await proxy('GET', f'{PRODUCTS_SERVICE}/products/{product_id}')


@app.get('/orders')
async def get_orders():
    return await proxy('GET', f'{ORDERS_SERVICE}/orders')


@app.post('/orders')
async def create_order(order: dict):
    return await proxy('POST', f'{ORDERS_SERVICE}/orders', order)


@app.get('/customers')
async def get_customers():
    return await proxy('GET', f'{CUSTOMERS_SERVICE}/customers')


@app.get('/customers/{customer_id}')
async def get_customer(customer_id: int):
    return await proxy('GET', f'{CUSTOMERS_SERVICE}/customers/{customer_id}')
