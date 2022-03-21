def calc_distance_in_pow_multi_attributes(attributes1: list[float], attributes2: list[float], power):
    distance = 0
    for i in range(len(attributes1)):
        distance += pow(abs(attributes1[i] - attributes2[i]), power)
    return pow(distance, 1 / power)


def calc_distance_in_pow(attribute1: float, attribute2: float, power: float):
    distance = pow(abs(attribute1 - attribute2), power)
    return pow(distance, 1 / power)
