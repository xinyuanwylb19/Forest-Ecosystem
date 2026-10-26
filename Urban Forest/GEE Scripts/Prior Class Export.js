// Created on Oct 13, 2026.
// Author: Xinyuan Wei.
// Annual MODIS tree cover of the land that joined each urban center, split by its settlement class at the
// previous epoch (rural classes 10 to 13 or urban cluster classes 21 to 23). Companion of Annual Canopy Export.js.

// ------------------------------------------------------------------------------------------
// 1. Parameters.
// ------------------------------------------------------------------------------------------

var Epochs = [2000, 2005, 2010, 2015, 2020];
var Years = [];
for (var y = 2000; y <= 2024; y++) { Years.push(y); }
var Smod = "JRC/GHSL/P2023A/GHS_SMOD_V2-0/";
var Export_Folder = "Urban Forest Carbon";
var Export_Name = "Cohort Canopy Prior";

// ------------------------------------------------------------------------------------------
// 2. Urban centers of 2020, the cohort of each cell, and its class at the previous epoch.
// ------------------------------------------------------------------------------------------

var smod = Epochs.map(function (year) {
  return ee.Image(Smod + year).select("smod_code");
});
var masks = smod.map(function (image) { return image.eq(30); });
var proj = masks[0].projection();
var cohort = ee.Image(0);
for (var i = Epochs.length - 1; i >= 0; i--) {
  cohort = cohort.where(masks[i], i + 1);
}
cohort = cohort.updateMask(masks[4]);

// Prior class group of each cell, 1 for rural classes and 2 for urban cluster classes at the epoch before.
var prior = ee.Image(0);
for (var j = 1; j < Epochs.length; j++) {
  var before = smod[j - 1];
  prior = prior.where(cohort.eq(j + 1).and(before.lte(13)), 1);
  prior = prior.where(cohort.eq(j + 1).and(before.gte(21)).and(before.lte(23)), 2);
}
var subcohort = cohort.multiply(10).add(prior).updateMask(cohort.gte(2));

var centers = masks[4].selfMask().reduceToVectors({
  geometry: ee.Geometry.Rectangle([-180, -89, 180, 89], null, false),
  scale: 1000,
  crs: proj,
  eightConnected: true,
  geometryType: "polygon",
  labelProperty: "center",
  maxPixels: 1e13
});
centers = centers.map(function (f) {
  var c = f.geometry().centroid(1).transform("EPSG:4326", 1).coordinates();
  return f.set({lon: c.get(0), lat: c.get(1)});
});

// ------------------------------------------------------------------------------------------
// 3. Annual tree-covered area of each subcohort.
// ------------------------------------------------------------------------------------------

var vcf = ee.ImageCollection("MODIS/061/MOD44B");
var tree_proj = vcf.first().projection();
var area = ee.Image.pixelArea();
var bands = [];
var layers = [];
var codes = [];
for (var c = 2; c <= 5; c++) {
  for (var g = 1; g <= 2; g++) {
    codes.push([c, g]);
    layers.push(area.updateMask(subcohort.eq(c * 10 + g)).rename("a_" + c + "_" + g));
    bands.push("a_" + c + "_" + g);
  }
}
for (var k = 0; k < Years.length; k++) {
  var tree = ee.Image(vcf.filter(ee.Filter.calendarRange(Years[k], Years[k], "year")).first())
    .select("Percent_Tree_Cover");
  tree = tree.updateMask(tree.lte(100)).divide(100).multiply(area);
  for (var m = 0; m < codes.length; m++) {
    var name = "k_" + Years[k] + "_" + codes[m][0] + "_" + codes[m][1];
    layers.push(tree.updateMask(subcohort.eq(codes[m][0] * 10 + codes[m][1])).rename(name));
    bands.push(name);
  }
}
var result = ee.Image.cat(layers).reduceRegions({
  collection: centers,
  reducer: ee.Reducer.sum(),
  scale: 231.656358,
  crs: tree_proj,
  tileScale: 4
});

// ------------------------------------------------------------------------------------------
// 4. Export.
// ------------------------------------------------------------------------------------------

Export.table.toDrive({
  collection: result,
  description: "Cohort_Canopy_Prior",
  folder: Export_Folder,
  fileNamePrefix: Export_Name,
  fileFormat: "CSV",
  selectors: ["system:index", "lon", "lat"].concat(bands)
});
