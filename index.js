
var turf = require('turf');
var fs = require('fs');



var nyc_bbox = [-79.7625122070312, 40.4773979187012, -71.8527069091797, 45.0158615112305];
var nj_bbox = [-75.5633926391602, 38.7887535095215, -73.8850555419922, 41.3574256896973];

var cellWidth = 5;
var units = 'miles';
 
//create hex grid and count points within each cell
var hexgrid_nyc = turf.hexGrid(nyc_bbox, cellWidth, units);
var hexgrid_nj = turf.hexGrid(nj_bbox, cellWidth, units);
 
for (var x = 0; x < Object.keys(hexgrid_nyc.features).length; x++) {
 hexgrid_nyc.features[x].properties['pt_count'] = x;
}

for (var x = 0; x < Object.keys(hexgrid_nj.features).length; x++) {
 hexgrid_nj.features[x].properties['pt_count'] = x;
}

 
fs.writeFileSync('./nyc_hex.geojson', JSON.stringify(hexgrid_nyc));
fs.writeFileSync('./nj_hex.geojson', JSON.stringify(hexgrid_nj));