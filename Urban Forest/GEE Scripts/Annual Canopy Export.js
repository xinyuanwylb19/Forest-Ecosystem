// Created on Oct 13, 2026.
// Author: Xinyuan Wei.
// Annual MODIS tree cover of every urban center and urbanization cohort, 2000 to 2024.
// Run in the Earth Engine Code Editor and start the export task in the Tasks tab.

// ------------------------------------------------------------------------------------------
// 1. Parameters.
// ------------------------------------------------------------------------------------------

var Epochs = [2000, 2005, 2010, 2015, 2020];
var Years = [];
for (var y = 2000; y <= 2024; y++) { Years.push(y); }
var Smod = "JRC/GHSL/P2023A/GHS_SMOD_V2-0/";
var Export_Folder = "Urban Forest Carbon";
var Export_Name = "Cohort Canopy Annual";

// RESOLVE biome numbers grouped into five classes.
var Biome_From = [1, 3, 9, 14, 2, 7, 4, 5, 8, 10, 12, 6, 11, 13];
var Biome_To = [1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4, 5];

// ------------------------------------------------------------------------------------------
// 2. Urban centers of 2020 and the urbanization cohort of each cell.
// ------------------------------------------------------------------------------------------

// Urban center masks (class 30) at each epoch.
var masks = Epochs.map(function (year) {
  return ee.Image(Smod + year).select("smod_code").eq(30);
});
var proj = masks[0].projection();

// Cohort 1 is land that was urban center in 2000, cohort 5 is land that became urban center by 2020.
var cohort = ee.Image(0);
for (var i = Epochs.length - 1; i >= 0; i--) {
  cohort = cohort.where(masks[i], i + 1);
}
cohort = cohort.updateMask(masks[4]).rename("cohort");

// Polygons of the 2020 urban centers, eight connected.
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
// 3. Biome and country of each urban center.
// ------------------------------------------------------------------------------------------

var biome = ee.Image().paint(ee.FeatureCollection("RESOLVE/ECOREGIONS/2017"), "BIOME_NUM")
  .remap(Biome_From, Biome_To).rename("biome");
var countries = ee.FeatureCollection("FAO/GAUL/2015/level0");
var adm0 = ee.Image().paint(countries, "ADM0_CODE").rename("adm0");
centers = biome.addBands(adm0).reduceRegions({
  collection: centers,
  reducer: ee.Reducer.mode(),
  scale: 1000,
  crs: proj
});
centers = centers.map(function (f) {
  var code = ee.Algorithms.If(f.get("adm0"), ee.Number(f.get("adm0")).round().toInt(), -1);
  return f.set("adm0", code);
});

// ------------------------------------------------------------------------------------------
// 4. Annual tree-covered area of each cohort.
// ------------------------------------------------------------------------------------------

var vcf = ee.ImageCollection("MODIS/061/MOD44B");
var tree_proj = vcf.first().projection();
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
var result = image.reduceRegions({
  collection: centers,
  reducer: ee.Reducer.sum(),
  scale: 231.656358,
  crs: tree_proj,
  tileScale: 4
});

// ------------------------------------------------------------------------------------------
// 5. Country names and export.
// ------------------------------------------------------------------------------------------

var joined = ee.Join.saveFirst({matchKey: "match", outer: true}).apply(result, countries,
  ee.Filter.equals({leftField: "adm0", rightField: "ADM0_CODE"}));
result = joined.map(function (f) {
  var name = ee.Algorithms.If(f.get("match"), ee.Feature(f.get("match")).get("ADM0_NAME"), "");
  return f.set("country", name);
});
Export.table.toDrive({
  collection: result,
  description: "Cohort_Canopy_Annual",
  folder: Export_Folder,
  fileNamePrefix: Export_Name,
  fileFormat: "CSV",
  selectors: ["system:index", "lon", "lat", "country", "adm0", "biome"].concat(bands)
});
