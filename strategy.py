import analyzer
import logging
import collections
import point_extractor

class MinimumDomainFirstStrategy:

    def __init__(self, interval_points, threshold = 0):
        super().__init__()
        self.interval_points = interval_points
        self.threshold = threshold

    def execute(self, sliding_window):
        points_to_process = list(filter(lambda item: 2 * item + 1 <= len(sliding_window), self.interval_points))
        logging.info("interval points to process: {points_to_process}".format(points_to_process = points_to_process))

        if len(points_to_process) == 0:
            return None

        points = point_extractor.extract_points(sliding_window, points_to_process)
        logging.info("extracted points for each interval: {points}".format(points = points))
        for point in points:
            threshold = self.threshold[point] if isinstance(self.threshold, collections.Mapping) else self.threshold
            if analyzer.is_local_max(points[point], threshold):
                logging.info("point {point} of domain {domain} is local max".format(point = points[point], domain = point))
                return 'SELL'
            elif analyzer.is_local_min(points[point], threshold):
                logging.info("point {point} of domain {domain} is local min".format(point = points[point], domain = point))
                return 'BUY'
        return None