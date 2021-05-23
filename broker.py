import requests
import config
from datetime import datetime
import hmac
import hashlib
import logging

api_base_url = config.api_base_url
api_key = config.api_key
secret_key = config.secret_key
samples_per_min = config.samples_per_min
symbol = config.symbol
interval_points = config.interval_points
threshold = config.threshold

def get_symbol_price(symbol):
    response = requests.get(config.api_base_url + "/v3/ticker/price", params={'symbol': symbol}, headers={'X-MBX-APIKEY': config.api_key})
    if response.status_code != 200:
        raise Exception({'code': response.status_code, 'msg': response.reason})
    return response

def get_service_info():
    response = requests.get(config.api_base_url + "/v3/exchangeInfo")
    if response.status_code != 200:
        raise Exception({'code': response.status_code, 'msg': response.reason})
    return response

def get_symbols():
    response = get_service_info()
    symbols = []
    for symbol in response.json()['symbols']:
        symbols.append(symbol['symbol'])
    return symbols

def place_order(symbol, side, quantity, price):
    timestamp = int(str(int(datetime.now().timestamp())) + '000')
    params = "symbol={symbol}&side={side}&type={type}&timeInForce={timeInForce}&quantity={quantity}&price={price}&recvWindow={recvWindow}&timestamp={timestamp}".format(symbol = symbol, side = side, type = "LIMIT", timeInForce = "GTC", quantity = quantity, price = price, recvWindow = 5000, timestamp = timestamp).encode('UTF-8')
    signature = hmac.new(secret_key, params, hashlib.sha256).hexdigest()
    logging.info("params: {params}, signature: {signature}".format(params = params, signature = signature))
    response = requests.post(api_base_url + "/v3/order", params={'symbol': symbol, 'side': side, 'type': 'LIMIT', 'timeInForce': 'GTC', 'quantity': quantity, 'price': price, 'recvWindow': 5000, 'timestamp': timestamp, 'signature': signature}, headers={'X-MBX-APIKEY': api_key})
    logging.info(response.json())
    if response.status_code != 200:
        raise Exception({'code': response.json()['code'], 'msg': response.json()['msg']})
    return response

def query_order(symbol, order_id):
    timestamp = int(str(int(datetime.now().timestamp())) + '000')
    params = "symbol={symbol}&orderId={order_id}&timestamp={timestamp}".format(symbol = symbol, order_id = order_id, timestamp = timestamp).encode('UTF-8')
    signature = hmac.new(secret_key, params, hashlib.sha256).hexdigest()
    logging.info("params: {params}, signature: {signature}".format(params = params, signature = signature))
    response = requests.get(api_base_url + "/v3/order", params={'symbol': symbol, 'orderId': order_id, 'timestamp': timestamp, 'signature': signature}, headers={'X-MBX-APIKEY': api_key})
    logging.info(response.json())
    if response.status_code != 200:
        raise Exception({'code': response.json()['code'], 'msg': response.json()['msg']})
    return response

def cancel_order(symbol, order_id):
    timestamp = int(str(int(datetime.now().timestamp())) + '000')
    params = "symbol={symbol}&orderId={order_id}&timestamp={timestamp}".format(symbol = symbol, order_id = order_id, timestamp = timestamp).encode('UTF-8')
    signature = hmac.new(secret_key, params, hashlib.sha256).hexdigest()
    logging.info("params: {params}, signature: {signature}".format(params = params, signature = signature))
    response = requests.delete(api_base_url + "/v3/order", params={'symbol': symbol, 'orderId': order_id, 'timestamp': timestamp, 'signature': signature}, headers={'X-MBX-APIKEY': api_key})
    logging.info(response.json())
    if response.status_code != 200:
        raise Exception({'code': response.json()['code'], 'msg': response.json()['msg']})
    return response
