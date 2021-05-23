import analyzer
import unittest
from sliding_window import SlidingWindow
import point_extractor

class AnalyzerTest(unittest.TestCase):

    def test_local_max_stable_no_thres(self):
        point = {'left': 1.32, 'mid': 1.32, 'right': 1.32}
        self.assertTrue(analyzer.is_local_max(point, 0) == False, "point {point} is no local max".format(point = point))

    def test_local_max_asc_no_thres(self):
        point = {'left': 1.32, 'mid': 1.33, 'right': 1.35}
        self.assertTrue(analyzer.is_local_max(point, 0) == False, "point {point} is no local max".format(point = point))

    def test_local_max_desc_no_thres(self):
        point = {'left': 1.32, 'mid': 1.31, 'right': 1.30}
        self.assertTrue(analyzer.is_local_max(point, 0) == False, "point {point} is no local max".format(point = point))

    def test_local_max_no_thres(self):
        point = {'left': 1.32, 'mid': 1.33, 'right': 1.30}
        self.assertTrue(analyzer.is_local_max(point, 0) == True, "point {point} is local max".format(point = point))

    def test_local_max_stable_thres(self):
        point = {'left': 1.32, 'mid': 1.32, 'right': 1.32}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_max(point, threshold) == False, "point {point} is no local max with threshold {threshold}".format(point = point, threshold = threshold))

    def test_local_max_asc_thres(self):
        point = {'left': 1.32, 'mid': 1.33, 'right': 1.35}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_max(point, threshold) == False, "point {point} is no local max with threshold {threshold}".format(point = point, threshold = threshold))

    def test_local_max_desc_thres(self):
        point = {'left': 1.32, 'mid': 1.31, 'right': 1.30}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_max(point, threshold) == False, "point {point} is no local max with threshold {threshold}".format(point = point, threshold = threshold))

    def test_local_max_not_enough_thres(self):
        point = {'left': 1.32, 'mid': 1.329, 'right': 1.30}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_max(point, threshold) == False, "point {point} is no local max with threshold {threshold}".format(point = point, threshold = threshold))

    def test_local_max_thres(self):
        point = {'left': 1.32, 'mid': 1.3333, 'right': 1.30}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_max(point, threshold) == True, "point {point} is local max with threshold {threshold}".format(point = point, threshold = threshold))

    def test_local_min_stable_no_thres(self):
        point = {'left': 1.32, 'mid': 1.32, 'right': 1.32}
        self.assertTrue(analyzer.is_local_min(point, 0) == False, "point {point} is no local min".format(point = point))

    def test_local_min_asc_no_thres(self):
        point = {'left': 1.32, 'mid': 1.33, 'right': 1.35}
        self.assertTrue(analyzer.is_local_min(point, 0) == False, "point {point} is no local min".format(point = point))

    def test_local_min_desc_no_thres(self):
        point = {'left': 1.32, 'mid': 1.31, 'right': 1.30}
        self.assertTrue(analyzer.is_local_min(point, 0) == False, "point {point} is no local min".format(point = point))

    def test_local_min_no_thres(self):
        point = {'left': 1.32, 'mid': 1.30, 'right': 1.31}
        self.assertTrue(analyzer.is_local_min(point, 0) == True, "point {point} is local min".format(point = point))

    def test_local_min_stable_thres(self):
        point = {'left': 1.32, 'mid': 1.32, 'right': 1.32}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_min(point, threshold) == False, "point {point} is no local min with threshold {threshold}".format(point = point, threshold = threshold))

    def test_local_min_asc_thres(self):
        point = {'left': 1.32, 'mid': 1.33, 'right': 1.35}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_min(point, threshold) == False, "point {point} is no local min with threshold {threshold}".format(point = point, threshold = threshold))

    def test_local_min_desc_thres(self):
        point = {'left': 1.32, 'mid': 1.31, 'right': 1.30}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_min(point, threshold) == False, "point {point} is no local min with threshold {threshold}".format(point = point, threshold = threshold))

    def test_local_min_not_enough_thres(self):
        point = {'left': 1.32, 'mid': 1.31, 'right': 1.33}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_min(point, threshold) == False, "point {point} is no local min with threshold {threshold}".format(point = point, threshold = threshold))

    def test_local_min_thres(self):
        point = {'left': 1.355, 'mid': 1.31, 'right': 1.33}
        threshold = 0.01
        self.assertTrue(analyzer.is_local_min(point, threshold) == True, "point {point} is local min with threshold {threshold}".format(point = point, threshold = threshold))

class SlidingWindowTest(unittest.TestCase):

    def test_empty(self):
        sliding_window = SlidingWindow(10)
        self.assertEqual(len(sliding_window), 0, "len of empty sliding window must be 0")

    def test_item_count(self):
        sliding_window = SlidingWindow(10)
        sliding_window.add(4)
        sliding_window.add(53)
        self.assertEqual(len(sliding_window), 2, "sliding window must have 2 items")

    def test_clear(self):
        sliding_window = SlidingWindow(10)
        sliding_window.add(4)
        sliding_window.add(53)
        sliding_window.clear()
        self.assertEqual(len(sliding_window), 0, "sliding window after clear must have 0 items")

    def test_window_side(self):
        sliding_window = SlidingWindow(2)
        sliding_window.add(4)
        sliding_window.add(53)
        sliding_window.add(5)
        self.assertEqual(len(sliding_window), 2, "sliding window must have less or equal number of items than sliding window size")

class PointExtractorTest(unittest.TestCase):

    def test_sliding_window_size_not_enough(self):
        sliding_window = SlidingWindow(20)
        edge_sizes = [1, 5]
        with self.assertRaises(Exception):
            point_extractor.extract_points(sliding_window, edge_sizes)

    def test_datapoints_number(self):
        sliding_window = SlidingWindow(20)
        edge_sizes = [1, 5]
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        size_datapoints = point_extractor.extract_points(sliding_window, edge_sizes)
        self.assertEqual(len(size_datapoints), 2)

    def test_datapoints_avg(self):
        sliding_window = SlidingWindow(20)
        edge_sizes = [1, 5]
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        sliding_window.add(1)
        size_datapoints = point_extractor.extract_points(sliding_window, edge_sizes)
        self.assertTrue(size_datapoints[1]['left'] == 1 and size_datapoints[1]['right'] == 1 and size_datapoints[5]['left'] == 1 and size_datapoints[5]['right'] == 1) 



if __name__ == '__main__':
    unittest.main()