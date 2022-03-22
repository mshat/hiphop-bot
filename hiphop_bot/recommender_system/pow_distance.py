def calc_distance_in_pow(attribute1: float, attribute2: float, power: float):
    distance = pow(abs(attribute1 - attribute2), power)
    return pow(distance, 1 / power)
