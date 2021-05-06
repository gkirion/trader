import analyzer
import logging

class MinimumDomainFirstStrategy:

    def __init__(self, points, threshold):
        super().__init__()
        self.points = points
        self.threshold = threshold

    def execute(self):
        for point in self.points:
            if analyzer.is_local_max(self.points[point], self.threshold):
                logging.info("point {point} of domain {domain} is local max".format(point = self.points[point], domain = point))
                return 'SELL'
            elif analyzer.is_local_min(self.points[point], self.threshold):
                logging.info("point {point} of domain {domain} is local min".format(point = self.points[point], domain = point))
                return 'BUY'
        return None