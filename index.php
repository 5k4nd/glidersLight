<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8' />
    <title></title>
    <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />
    <script src='https://api.tiles.mapbox.com/mapbox-gl-js/v0.39.1/mapbox-gl.js'></script>
    <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v0.39.1/mapbox-gl.css' rel='stylesheet' />
    <style>
        body { margin:0; padding:0; }
        #map { position:absolute; top:0; bottom:0; width:100%; }
    </style>
</head>
<body>

<div id='map'></div>
<script>
mapboxgl.accessToken = 'pk.eyJ1IjoibGl0dGxlZGFkIiwiYSI6ImNqNWEzcXIyOTJjeDczM2x5YmdobWhtNzUifQ.P2AKGG6CVh9ixDCO9UN_4g';
    var map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/littledad/cj5a5xhlk1lop2snw9qpr0gof',
        center: [-74.50, 40], // starting position [lng, lat]
        zoom: 2 // starting zoom
    });

    var url = 'https://wanderdrone.appspot.com/';
    map.on('load', function () {
        window.setInterval(function() {
            map.getSource('drone').setData(url);
        }, 2000);

        map.addSource('drone', { type: 'geojson', data: url }); 
        map.addLayer({
            "id": "drone",
            "type": "symbol",
            "source": "drone",
            "layout": {
                "icon-image": "rocket-15"
            }   
        }); 
    });
</script>

</body>
</html>

