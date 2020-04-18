const modal = require("./modal.json");

const currentYearLayer = modal.layers[2].currentYearEarnings;
const layerKeys = Object.keys(modal.layers[0]);

const anonymous = input => {
    let totalLayers = 0;

    for (const layerKey of Object.keys(modal.layers[1])) {
        const relevantLayer = modal.layers[1][layerKey];
        const relevantLayerTotal =
            relevantLayer.bias +
            layerKeys.reduce((prev, curr) => {
                return prev + relevantLayer.weights[curr] * (input[curr] || 0);
            }, 0);

        totalLayers +=
            currentYearLayer.weights[layerKey] /
            (1 + 1 / Math.tanh(relevantLayerTotal));
    }
    let currentYearEarnings =
        1 / (1 + 1 / Math.tanh(currentYearLayer.bias + totalLayers));

    return {currentYearEarnings};
};

// Validation
console.log(
    anonymous({
        "gova_simplex_2019": 0.01691,
        "lastYearEarnings": 0.06,
        "max_height": 0.02892,
        "min_height": 0.01201,
        "ms_komot": 0.04,
        "neighborhoodName": 0.1
    })
);

console.log(
    anonymous({
        ms_komot: 0.01,
        gova_simplex_2019: 0.008230000000000001,
        max_height: 0.0349,
        min_height: 0.026670000000000003,
        lastYearEarnings: 0.01,
        neighborhoodName: 0.15
    })
);