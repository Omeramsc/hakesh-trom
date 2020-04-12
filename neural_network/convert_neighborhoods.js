const fs = require("fs");
const parse = require("csv-parse/lib/sync");

const cleanRecord = (data) => {
    const {gova_simplex_2019, ms_komot, max_height, min_height, lastYearEarnings, currentYearEarnings, neighborhoodName} = data;
    return {
        attributes: {gova_simplex_2019, ms_komot, max_height, min_height},
        geometry: JSON.parse(data.geometry),
        lastYearEarnings,
        currentYearEarnings,
        neighborhoodName
    }
}

const rawData = parse(fs.readFileSync("../tlv_data/datatlv.csv"), {
    columns: true,
    skip_empty_lines: true
});

const cleanedData = rawData.map(cleanRecord);
fs.writeFileSync("output/buildings.json", JSON.stringify(cleanedData));