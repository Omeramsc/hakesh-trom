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
            (1 + 1 / Math.exp(relevantLayerTotal));
    }
    let currentYearEarnings =
        1 / (1 + 1 / Math.exp(currentYearLayer.bias + totalLayers));

    return {currentYearEarnings};
};

console.log(
    anonymous({
        gova_simplex_2019: 0.1,
        ms_komot: 0.03,
        max_height: 0.01,
        min_height: 0.01,
        lastYearEarnings: 0.1,
        neighborhoodName: 0.28
    })
);