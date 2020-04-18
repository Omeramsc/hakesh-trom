const polylabel = require('polylabel');
const fs = require('fs');
const buildingsData = require('../reverse-geo-location/output/buildings_with_addresses.json');
const neighborhoodsData = require('../seed_data/neighborhoods.json')


const formatBuilding = (building) => {
    const deepCloneBuilding = JSON.parse(JSON.stringify(building))

    deepCloneBuilding.geometry = JSON.parse(deepCloneBuilding.geometry)
    deepCloneBuilding.centerPoint = polylabel([deepCloneBuilding.geometry], 1.0)

    return deepCloneBuilding;
}
const formatNeighborhood = (neighborhood) => {
    const deepCloneNeighborhood = JSON.parse(JSON.stringify(neighborhood))
    deepCloneNeighborhood.attributes.centerPoint = polylabel(deepCloneNeighborhood.geometry.rings, 1.0)

    return deepCloneNeighborhood;
}


const formattedBuildingsData = buildingsData.map(formatBuilding)
const formattedNeighborhoodsData = {...neighborhoodsData, features: neighborhoodsData.features.map(formatNeighborhood)}

fs.writeFileSync("output/buildings_with_addresses_center.json", JSON.stringify(formattedBuildingsData));
fs.writeFileSync("output/neighborhoods_with_center.json", JSON.stringify(formattedNeighborhoodsData));


