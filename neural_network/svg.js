const fs = require("fs");
const brain = require("brain.js");
const modal = require("./output/modal.json");

const response = brain.utilities.toSVG(modal);
fs.writeFileSync("output/vis.svg", response);
