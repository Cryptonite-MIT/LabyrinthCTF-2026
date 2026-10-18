# 29. Hecate Was Here

Author: Hitu1197

Phase 3 | osint

Flag: `labyrinth{telephoning.swatting.winemaker}`

## Description

Is it even a crossroad?
Format: labyrinth{xxx.xxx.xxx}

## Solve

- If you either check vegetation or road, it looks similar to Africa
- You can use any car meta websites to find this car, and it shows as the famous Ghana car
- Now that country is known, just use a website like plonkit or other documentation, after reading a bit, the road looks like the south captured path
- If you look through few roads, you find one with this particular car, and similar red path color
- Travel a bit on that and you get coords: `5.3862106,-1.9394877`
- Go to what3words (inferred from flag format, or past geosint chall) and put coords to get: `telephoning.swatting.winemaker`
