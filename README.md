# Maptiles for PeriodO maps

Makes tiles from Natural Earth data for use in the [PeriodO client](https://github.com/periodo/periodo-client#readme).
We currently use the [cross blended hypso with shaded relief, water, and drainages](https://www.naturalearthdata.com/downloads/10m-cross-blend-hypso/cross-blended-hypso-with-shaded-relief-water-and-drainages/).

To make tiles:

1. Install [GDAL](https://gdal.org) with Python support.
1. Make sure the `python3` executable with access to the GDAL libs is in your path.
1. Run `make all`.

This should download the data from Natural Earth and create a
directory with the following structure:
```
maptiles/
├── 0
│   └──   1  (1×1) tile
├── 1
│   └──  32  (8×4) tiles
├── 2
│   └── 128 (16×8) tiles
└── manifest.json
```
