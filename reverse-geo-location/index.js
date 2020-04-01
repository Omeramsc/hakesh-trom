const axios = require("axios");
const fs = require("fs");
const parse = require("csv-parse/lib/sync");
const polylabel = require("polylabel");

const URL = `https://maps.googleapis.com/maps/api/geocode/json`;
const LANGUAGE = "iw";

function getCenterPoint(row) {
    const points = JSON.parse(row.geometry);

    return polylabel([points], 1.0);
}

function outputData(data) {
    fs.writeFileSync("./output/buildings_with_addresses.json", JSON.stringify(data));
}

async function getAddresses() {
    if (!process.env.GOOGLE_API_KEY) {
        console.log(
            "Can't find GOOGLE_API_KEY, please add GOOGLE_API_KEY as an env var"
        );
        process.exit(1);
    }

    console.time("Runtime");

    const rawData = parse(fs.readFileSync("../tlv_data/datatlv.csv"), {
        columns: true,
        skip_empty_lines: true
    });

    const updatedData = [];
    let successSearches = 0;
    let failedSearches = 0;

    console.log(`Will search for ${rawData.length} addresses`);

    for (const row of rawData) {
        const rowIndex = successSearches + failedSearches + 1;
        console.log(
            `Starting to work on record ${rowIndex}.\tOK: ${successSearches}  FAILED: ${failedSearches} LEFT: ${rawData.length - rowIndex}`
        );
        let formattedAddress = "UNKNOWN";
        const centerPoint = getCenterPoint(row);

        try {
            const response = await axios.get(URL, {
                params: {
                    key: process.env.GOOGLE_API_KEY,
                    language: LANGUAGE,
                    latlng: centerPoint.reverse().join(",")
                }
            });
            if (response.data.results) {
                formattedAddress = response.data.results[0].formatted_address;
                successSearches++;
            } else {
                failedSearches++;
            }
        } catch (err) {
            console.error(err);
            failedSearches++;
        }

        updatedData.push({...row, formattedAddress});
    }

    outputData(updatedData);
    console.timeEnd("Runtime")
}

getAddresses();