NE = www.naturalearthdata.com
NE_URL := https://$(NE)/http//$(NE)/download/10m/raster

# Natural Earth II with shaded relief, water, and drainages, hi-res
SOURCE_DATA = NE2_HR_LC_SR_W_DR

# Cross blended hypso with shaded relief, water, and drainages, hi-res
# SOURCE_DATA = HYP_HR_SR_W_DR

$(SOURCE_DATA).zip:
	curl -L $(NE_URL)/$@ > $@

$(SOURCE_DATA).tif: $(SOURCE_DATA).zip
	unzip -p $< $(SOURCE_DATA)/$@ > $@

maptiles/manifest.json: $(SOURCE_DATA).tif
	./make-tiles.py $<
	find maptiles -name "*.xml" -exec rm -f {} \; # don't need these

.PHONY: all clean

.PRECIOUS: $(SOURCE_DATA).zip

all: maptiles/manifest.json

clean:
	rm -rf maptiles $(SOURCE_DATA).tif
