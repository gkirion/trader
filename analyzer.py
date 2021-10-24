def is_local_max(point, threshold):
    if point['mid'] - point['left'] > point['left'] * threshold:
        if point['mid'] - point ['right'] > point['right'] * threshold:
            return True
    return False

def is_local_min(point, threshold):
    if point['mid'] - point['left'] < -point['left'] * threshold:
        if point['mid'] - point['right'] < -point['right'] * threshold:
            return True
    return False