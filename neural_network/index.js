const brain = require("brain.js");
const fs = require("fs");
const parse = require("csv-parse/lib/sync");

const neighborhoodsData = require("../tlv_data/neighborhoods.json");

const net = new brain.NeuralNetwork();

const OUTPUT = {
    attributeName: "currentYearEarnings",
    outputName: "currentYearEarnings"
};

const STANDARDIZE_NEIGHBORHOOD = Object.fromEntries(
    neighborhoodsData.features.map(n => [
        n.attributes.shem_shchuna,
        n.attributes.ms_shchuna / 100
    ])
);

const STANDARDIZE_INPUTS = {
    FLOORS: 100,
    EARNINGS: 1000,
    MIN_HEIGHT: 1000,
    MAX_HEIGHT: 1000,
    GOVA_SIMPLEX: 1000,
    STANDARDIZE_NEIGHBORHOOD: STANDARDIZE_NEIGHBORHOOD
};

const FILED_TO_STANDERIZER = {
    gova_simplex_2019: "GOVA_SIMPLEX",
    ms_komot: "FLOORS",
    max_height: "MAX_HEIGHT",
    min_height: "MIN_HEIGHT",
    lastYearEarnings: "EARNINGS",
    currentYearEarnings: "EARNINGS",
    neighborhoodName: "STANDARDIZE_NEIGHBORHOOD"
};

console.time();

const encode = (attributeName, value) => {
    if (FILED_TO_STANDERIZER[attributeName]) {
        const intValue = parseInt(value, 10);
        if (isNaN(intValue)) {
            return STANDARDIZE_INPUTS[FILED_TO_STANDERIZER[attributeName]][value];
        }

        return value / STANDARDIZE_INPUTS[FILED_TO_STANDERIZER[attributeName]];
    }

    return 0;
};

const decode = (attributeName, value) => {
    if (FILED_TO_STANDERIZER[attributeName]) {
        return value * STANDARDIZE_INPUTS[FILED_TO_STANDERIZER[attributeName]];
    }

    return 0;
};

const cleanRecord = record => {
    const cleanRecord = {...record};

    for (const key of Object.keys(cleanRecord)) {
        if (!FILED_TO_STANDERIZER[key]) {
            delete cleanRecord[key];
        }
    }

    return cleanRecord;
};

const encodeRecord = record => {
    const cleanRecord = {...record};

    for (const key of Object.keys(cleanRecord)) {
        cleanRecord[key] = encode(key, cleanRecord[key]);
    }

    return cleanRecord;
};

const buildNetworkRecord = record => {
    const input = {};
    const output = {};

    for (const key of Object.keys(record)) {
        if (OUTPUT.attributeName === key) {
            output[OUTPUT.outputName] = record[key];
        } else {
            input[key] = record[key];
        }
    }

    return {
        input,
        output
    };
};

const rawData = parse(fs.readFileSync("../tlv_data/datatlv.csv"), {
    columns: true,
    skip_empty_lines: true
});

const networkRecords = rawData
    .map(cleanRecord)
    .map(encodeRecord)
    .map(buildNetworkRecord);

net.train(networkRecords);

console.timeEnd();

fs.writeFileSync("output/function.js", net.toFunction().toString());
fs.writeFileSync("output/modal.json", JSON.stringify(net.toJSON()));