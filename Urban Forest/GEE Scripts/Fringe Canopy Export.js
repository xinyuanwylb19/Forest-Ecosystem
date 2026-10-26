// Created on Oct 13, 2026.
// Author: Xinyuan Wei.
// Annual MODIS tree cover of all settlement land (GHS-SMOD classes 21 to 30) by the epoch at which rural land
// first became settlement, summed by country and by ecoregion. Companion of Annual Canopy Export.js.

// ------------------------------------------------------------------------------------------
// 1. Parameters.
// ------------------------------------------------------------------------------------------

var Epochs = [2000, 2005, 2010, 2015, 2020];
var Years = [];
for (var y = 2000; y <= 2024; y++) { Years.push(y); }
var Smod = "JRC/GHSL/P2023A/GHS_SMOD_V2-0/";
var Export_Folder = "Urban Forest Carbon";

// ------------------------------------------------------------------------------------------
// 2. Settlement land of 2020 and the epoch at which each cell first became settlement.
// ------------------------------------------------------------------------------------------

var masks = Epochs.map(function (year) {
  return ee.Image(Smod + year).select("smod_code").gte(21);
});
var cohort = ee.Image(0);
for (var i = Epochs.length - 1; i >= 0; i--) {
  cohort = cohort.where(masks[i], i + 1);
}
cohort = cohort.updateMask(masks[4]);

// ------------------------------------------------------------------------------------------
// 3. Annual tree-covered area of each cohort.
// ------------------------------------------------------------------------------------------

var vcf = ee.ImageCollection("MODIS/061/MOD44B");
var area = ee.Image.pixelArea();
var bands = [];
var layers = [];
for (var c = 1; c <= 5; c++) {
  layers.push(area.updateMask(cohort.eq(c)).rename("a_" + c));
  bands.push("a_" + c);
}
for (var k = 0; k < Years.length; k++) {
  var tree = ee.Image(vcf.filter(ee.Filter.calendarRange(Years[k], Years[k], "year")).first())
    .select("Percent_Tree_Cover");
  tree = tree.updateMask(tree.lte(100)).divide(100).multiply(area);
  for (var c2 = 1; c2 <= 5; c2++) {
    var name = "k_" + Years[k] + "_" + c2;
    layers.push(tree.updateMask(cohort.eq(c2)).rename(name));
    bands.push(name);
  }
}
var image = ee.Image.cat(layers);

// ------------------------------------------------------------------------------------------
// 4. Sums by country and by ecoregion on a geographic grid, which avoids edge errors of large polygons
// in the sinusoidal projection.
// ------------------------------------------------------------------------------------------

var countries = image.reduceRegions({
  collection: ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.neq("ADM0_NAME", "Antarctica")),
  reducer: ee.Reducer.sum(),
  scale: 231.656358,
  crs: "EPSG:4326",
  tileScale: 4
});
Export.table.toDrive({
  collection: countries,
  description: "Fringe_Canopy_Country",
  folder: Export_Folder,
  fileNamePrefix: "Fringe Canopy Country",
  fileFormat: "CSV",
  selectors: ["ADM0_NAME", "ADM0_CODE"].concat(bands)
});
var ecoregions = image.reduceRegions({
  collection: ee.FeatureCollection("RESOLVE/ECOREGIONS/2017"),
  reducer: ee.Reducer.sum(),
  scale: 231.656358,
  crs: "EPSG:4326",
  tileScale: 4
});
Export.table.toDrive({
  collection: ecoregions,
  description: "Fringe_Canopy_Biome",
  folder: Export_Folder,
  fileNamePrefix: "Fringe Canopy Biome",
  fileFormat: "CSV",
  selectors: ["ECO_NAME", "BIOME_NUM", "BIOME_NAME"].concat(bands)
});
