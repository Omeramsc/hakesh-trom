# Reverse Geo-location Search

From the TLV API we're getting the building polygon but we want get know the address name as well.
This is where the `Reverse Geo-location Search` come into play.

## Steps
1. Load the data
1. Calculate the center - We have the building polygon but we need to search by 1 geo-location point, this point will be the center of the building.
1. Preform Reverse Geo-location Search via Google Maps API
1. Output the data

## How to run

```bash
npm i
GOOGLE_API_KEY=<SECRET-KEY> node .
```