from sliding_window import SlidingWindow
from strategy import MinimumDomainFirstStrategy
import point_extractor
import analyzer
import logging
import sys
import time
import config
import broker
import json

api_base_url = config.api_base_url
api_key = config.api_key
secret_key = config.secret_key
samples_per_min = config.samples_per_min
symbol = config.symbol
interval_points = config.interval_points
threshold = config.threshold
order_threshold = config.order_threshold

logging.basicConfig(filename = 'trader_log.txt', format = '%(asctime)s - %(module)s - %(levelname)s - %(message)s', level = logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(consoleHandler)

logging.info("starting trader...")
logging.info("api base url: {api_base_url}, samples per min: {samples_per_min}, symbol: {symbol}, interval points: {interval_points}".format(api_base_url = api_base_url, samples_per_min = samples_per_min, symbol = symbol, interval_points = interval_points))
sliding_window = SlidingWindow(max(interval_points) * 2 + 1)

# load previous order
try:
    with open('previous_order.txt') as file:
        previous_order = json.loads(file.readline())
        logging.info("loaded previous order: {previous_order}".format(previous_order = previous_order))
except FileNotFoundError as e:
    previous_order = {'type': 'BUY', 'price': 1.16}
    logging.warning("{exception}, using default: {default}".format(exception = e, default = previous_order))


def extract_minute_average(samples_per_min = 10):
    number_of_samples = 0
    avg_price = 0.0
    while number_of_samples < samples_per_min:
        try:
            time.sleep(60 / samples_per_min)
            price = broker.get_symbol_price(symbol).json()['price']
            logging.info("sample: {sample}, price: {price} eur".format(sample = number_of_samples, price = price))
            avg_price += float(price)
            number_of_samples += 1
        except Exception as e:
            logging.warning(e)
    avg_price = avg_price / number_of_samples
    return avg_price


while True:
    avg_price = extract_minute_average(samples_per_min)
    logging.info("1 min average price: {avg_price} eur".format(avg_price = avg_price))
    sliding_window.add(avg_price)

    strategy = MinimumDomainFirstStrategy(interval_points, threshold)
    logging.info("using minimum domain first strategy")
    strategy_action = strategy.execute(sliding_window)
    logging.info("strategy action: {strategy_action}".format(strategy_action = strategy_action))

    if strategy_action != None:
        if 'status' in previous_order and 'orderId' in previous_order and previous_order['status'] != 'FILLED':
            try:
                response = broker.query_order('XRPEUR', previous_order['orderId']).json()
                previous_order['status'] = response['status']
                if response['status'] == 'FILLED':
                    previous_order['price'] = float(response['price'])
                    with open('previous_order.txt', 'w') as file:
                        file.write(json.dumps(previous_order))
            except Exception as e:
                logging.warning(e)

        new_order = {'type': strategy_action, 'price': round(float(avg_price), 4)}
        if new_order['type'] == 'BUY':
            if ('status' not in previous_order or previous_order['status'] == 'FILLED') and previous_order['type'] != 'BUY':
                if previous_order['price'] > new_order['price'] * (1 + order_threshold):
                    try:
                        response = broker.place_order('XRPEUR', 'BUY', 10, round(float(avg_price), 4)).json()
                        logging.info(response)
                        previous_order['orderId'] = response['orderId']
                        previous_order['status'] = response['status']
                        previous_order['type'] = 'BUY'
                        previous_order['price'] = float(response['price'])
                        if response['status'] == 'FILLED':
                            with open('previous_order.txt', 'w') as file:
                                file.write(json.dumps(previous_order))
                    except Exception as e:
                        logging.warning(e)

                else:
                    logging.info("new order price {new_order}, previous order price {previous_order}, skipping".format(new_order = new_order['price'], previous_order = previous_order['price']))
            else:
                logging.info("previous order was BUY too, skipping")

        elif new_order['type'] == 'SELL':
            if ('status' not in previous_order or previous_order['status'] == 'FILLED') and previous_order['type'] != 'SELL':
                if new_order['price'] > previous_order['price'] * (1 + order_threshold):
                    try:
                        response = broker.place_order('XRPEUR', 'SELL', 10, round(float(avg_price), 4)).json()
                        logging.info(response)
                        previous_order['orderId'] = response['orderId']
                        previous_order['status'] = response['status']
                        previous_order['type'] = 'SELL'
                        previous_order['price'] = float(response['price'])
                        if response['status'] == 'FILLED':
                            with open('previous_order.txt', 'w') as file:
                                file.write(json.dumps(previous_order))
                    except Exception as e:
                        logging.warning(e)
                else:
                    logging.info("new order price {new_order}, previous order price {previous_order}, skipping".format(new_order = new_order['price'], previous_order = previous_order['price']))
            else:
                logging.info("previous order was SELL too, skipping")
