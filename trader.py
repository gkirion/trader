from sliding_window import SlidingWindow
from strategy import MinimumDomainFirstStrategy
import point_extractor
import analyzer
import logging
import sys
import time
import config
import broker

api_base_url = config.api_base_url
api_key = config.api_key
secret_key = config.secret_key
samples_per_min = config.samples_per_min
symbol = config.symbol
interval_points = config.interval_points
threshold = config.threshold

logging.basicConfig(filename = 'trader_log.txt', format = '%(asctime)s - %(module)s - %(levelname)s - %(message)s', level = logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(consoleHandler)

logging.info("starting trader...")
logging.info("api base url: {api_base_url}, samples per min: {samples_per_min}, symbol: {symbol}, interval points: {interval_points}".format(api_base_url = api_base_url, samples_per_min = samples_per_min, symbol = symbol, interval_points = interval_points))

sliding_window = SlidingWindow(max(interval_points) * 2 + 1)
previous_order = {'type': 'BUY', 'price': 1.16}

while True:
    number_of_samples = 0
    avg_price = 0.0
    while number_of_samples < samples_per_min:
        price = broker.get_symbol_price(symbol).json()['price']
        logging.info("sample: {sample}, price: {price} eur".format(sample = number_of_samples, price = price))
        avg_price += float(price)
        number_of_samples += 1
        time.sleep(60 / samples_per_min)

    avg_price = avg_price / number_of_samples
    logging.info("1 min average price: {avg_price} eur".format(avg_price = avg_price))
    sliding_window.add(avg_price)

    points_to_process = list(filter(lambda point: 2 * point + 1 <= len(sliding_window), interval_points))
    logging.info("interval points to process: {points_to_process}".format(points_to_process = points_to_process))

    if len(points_to_process) > 0:
        points = point_extractor.extract_points(sliding_window, points_to_process)
        logging.info("extracted points for each interval: {points}".format(points = points))

        strategy = MinimumDomainFirstStrategy(points, threshold)
        logging.info("using minimum domain first strategy with threshold: {threshold}".format(threshold = threshold))
        strategy_action = strategy.execute()
        logging.info("strategy action: {strategy_action}".format(strategy_action = strategy_action))

        if strategy_action != None:
            new_order = {'type': strategy_action, 'price': round(avg_price, 4)}
            if new_order['type'] == 'BUY':
                if previous_order['type'] == None or previous_order['type'] != 'BUY':
                    if previous_order['price'] == None or previous_order['price'] > new_order['price']:
                        try:
                            response = broker.place_order('XRPEUR', 'BUY', 10, round(avg_price, 4))
                            logging.info(response.json())
                            while response.json()['status'] != 'FILLED':
                                time.sleep(2)
                                response = broker.query_order('XRPEUR', response.json()['orderId'])
                                logging.info(response.json())
                            previous_order['type'] = 'BUY'
                            previous_order['price'] = float(response.json()['price'])
                        except Exception as e:
                            logging.warn(e)
                    else:
                        logging.info("previous order price {previous_order_price} is lower or equal to current order price {current_order_price}, skipping".format(previous_order_price = previous_order['price'], current_order_price = new_order['price']))
                else:
                    logging.info("previous order was BUY too, skipping")

            elif new_order['type'] == 'SELL':
                if previous_order['type'] != 'SELL':
                    if previous_order['price'] < new_order['price']:
                        try:
                            response = broker.place_order('XRPEUR', 'SELL', 10, round(avg_price, 4))
                            logging.info(response.json())
                            while response.json()['status'] != 'FILLED':
                                time.sleep(2)
                                response = broker.query_order('XRPEUR', response.json()['orderId'])
                                logging.info(response.json())
                            previous_order['type'] = 'SELL'
                            previous_order['price'] = float(response.json()['price'])
                        except Exception as e:
                            logging.warn(e)
                    else:
                        logging.info("previous order price {previous_order_price} is higher or equal to current order price {current_order_price}, skipping".format(previous_order_price = previous_order['price'], current_order_price = new_order['price']))
                else:
                    logging.info("previous order was SELL too, skipping")
