def extract_points(sliding_window, edge_sizes):
    if len(sliding_window) < max(edge_sizes) * 2 + 1:
        raise Exception("size of sliding window must be greater than or equal to 2 * max_edge_size + 1")

    size_datapoints = {}
    sum = {}
    for edge_size in edge_sizes:
        size_datapoints[edge_size] = {}
        sum[edge_size] = 0.0
    i = 0
    for point in sliding_window:
        i += 1
        for edge_size in edge_sizes:
            sum[edge_size] += point
            if edge_size == i:
                size_datapoints[edge_size]['right'] = sum[edge_size] / edge_size
            elif edge_size + 1 == i:
                size_datapoints[edge_size]['mid'] = point
                sum[edge_size] = 0.0
            elif edge_size * 2 + 1 == i:
                size_datapoints[edge_size]['left'] = sum[edge_size] / edge_size
    return size_datapoints
