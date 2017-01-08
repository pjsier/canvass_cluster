var map;
var markerLayerGroup = L.layerGroup([]);
// https://github.com/dwnoble/LeafletHtmlIcon/blob/master/LeafletHtmlIcon.js
L.HtmlIcon = L.Icon.extend({
	options: {},
	initialize: function (options) {
		L.Util.setOptions(this, options);
	},
	createIcon: function () {
		var div = document.createElement('div');
		div.innerHTML = this.options.html;
		return div;
	},
	createShadow: function () {
		return null;
	}
});

var markerPath = document.createElement("path");
var svgStr = '<svg width="35" height="50" xmlns="http://www.w3.org/2000/svg" class="leaflet-marker-icon leaflet-zoom-animated leaflet-interactive">\
  <g>\
   <path d="m17.5,49.643177c0,0.009065 0.01813,0.027195 0.01813,0.027195s15.881864,-24.384826 15.881864,-32.398278c0,-11.793553 -8.049712,-16.924338 -15.899994,-16.942468c-7.850282,0.01813 -15.899994,5.148915 -15.899994,16.942468c0,8.013452 15.890929,32.398278 15.890929,32.398278s0.009065,-0.027195 0.009065,-0.027195zm-5.50245,-33.041892c0,-3.045837 2.465678,-5.511515 5.511515,-5.511515c3.045837,0 5.511515,2.465678 5.511515,5.511515s-2.474743,5.511515 -5.52058,5.511515c-3.036772,0 -5.50245,-2.465678 -5.50245,-5.511515z"/>\
  </g>\
</svg>'
var parser = new DOMParser();
var markerSvg = parser.parseFromString(svgStr, "text/html").querySelector("svg");

// Organized by section, deliberately mixing up now
var COLOR_ARR = [
  // Greens
  '#00441b',
  '#238b45',
  '#66c2a4',
  '#ccece6',
  // Purples
  '#4d004b',
  '#7a0177',
  '#810f7c',
  '#8c6bb1',
  // Red/Oranges
  '#7f0000',
  '#d7301f',
  '#fc8d59',
  '#fdd49e',
  // Blues
  '#08306b',
  '#2171b5',
  '#6baed6',
  '#ece7f2',
  // Pinks
  '#67001f',
  '#ce1256',
  '#df65b0',
  '#d4b9da'
];

var COLOR_OPTIONS = [
  '#00441b',
  '#4d004b',
  '#7f0000',
  '#08306b',
  '#67001f',
  '#238b45',
  '#7a0177',
  '#d7301f',
  '#2171b5',
  '#ce1256',
  '#66c2a4',
  '#810f7c',
  '#fc8d59',
  '#6baed6',
  '#df65b0',
  '#ccece6',
  '#fdd49e',
  '#ece7f2',
  '#d4b9da'
];

(function() {
  map = L.map('map');
  var osmUrl='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png';
  var osmAttrib='&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>';
  var osm = new L.TileLayer(osmUrl, {minZoom: 5, maxZoom: 18, attribution: osmAttrib});
  map.addLayer(osm);
  map.setView([41.907477, -87.685913], 10);

  document.querySelector("button").addEventListener("click", function(e) {
    var req = new XMLHttpRequest();
    req.open("POST", "/locations");
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.onload = function() {
      if (req.status === 200) {
        // handle response data
        markerLayerGroup.clearLayers();
        var respData = JSON.parse(req.responseText);
        var markers = respData.locations.map(function(p) {
          // Deep clone of svg string
          var svgNode = markerSvg.cloneNode(true);
          svgNode.querySelector("path").setAttribute("fill", COLOR_OPTIONS[p.group - 1]);

          var markerIcon = new L.HtmlIcon({html : svgNode.outerHTML});
          var m = L.marker([p.lat, p.lon], {icon: markerIcon});
          m.bindPopup('<p>Group: ' + p.group + '</p>' +
                      '<p>Address: ' + p.address + '</p>' +
                      '<p>ID: ' + p.id + '</p>' +
                      '<p>Created At ' + p.created_at + '</p>');
          return m;
        });
        markerLayerGroup = L.layerGroup(markers).addTo(map);
      }
    }
    req.send(JSON.stringify(test_data));
  });
})();
