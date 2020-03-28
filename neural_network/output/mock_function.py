import json
import math
import functools
import os


def load_network():
    modal_file_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modal.json')
    with open(modal_file_location) as json_file:
        return json.load(json_file)


modal = load_network()


def run_network(input):
    current_year_layer = modal["layers"][2]["currentYearEarnings"]
    known_layers_keys = modal["layers"][0].keys()
    total_layers = 0

    for layer_key in modal["layers"][1].keys():
        # Goes thru the layers and calculating the result
        relevant_layer = modal["layers"][1][layer_key]
        relevant_layer_total = relevant_layer["bias"] + functools.reduce(
            lambda prv, curr: prv + relevant_layer["weights"][curr] * input[curr],
            known_layers_keys, 0)

        # Adding the calculation of the layer with it's weight
        total_layers += current_year_layer["weights"][layer_key] / (1 + 1 / math.exp(relevant_layer_total))

    # Predict the current_year_earnings!
    current_year_earnings = 1 / (1 + 1 / math.exp(current_year_layer["bias"] + total_layers))
    return {'currentYearEarnings': current_year_earnings}


if __name__ == '__main__':
    print(run_network({
        'gova_simplex_2019': 0.1,
        'ms_komot': 0.03,
        'max_height': 0.01,
        'min_height': 0.01,
        'lastYearEarnings': 0.1,
        'neighborhoodName': 0.28
    }))
