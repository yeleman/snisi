
var COLOR_YES = '#78C201';
var COLOR_YES = '#C10E28';

// var COLORS = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#800026'];
var COLORS = ["#f7e0ad", "#fdc57a", "#f79359", "#d45844"];
// a2bec1
// var min = 0;
// var max = 1000;
// var indicator_name = "Indicateur ....";

var map;
var base_layer;
var info;
var geojson;
var health_areas_layer;
var legend;
var sidebar;
var sidebarBtn;

var geodata = {};

function getColor(value) {
    var diff = max - min;
    var levels = COLORS.length;
    var step = Math.ceil(diff / levels);

    var index = Math.floor((value - min) / step);
    return COLORS[index];
}

function median(values) {
    values.sort( function(a,b) {return a - b;} );

    var half = Math.floor(values.length/2);

    if(values.length % 2)
    return values[half];
    else
    return (values[half-1] + values[half]) / 2.0;
}

function quartiles(values) {
    values.sort( function(a,b) {return a - b;} );

    var med = median(values);
    // var lquartile = median(values[])


}

function getGrades() {
    var diff = max - min;
    var levels = COLORS.length;
    var step = Math.ceil(diff / levels);

    var g = min;
    var grades = [];
    while(g<max) {
        grades.push(g);
        g += step;
    }
    return grades;
}


function getYesNoColor(value) {
    if (value > 0)
        return COLOR_YES;
    return COLOR_NO;

}

function styleFeature(feature) {
    return {
        fillColor: getColor(feature.properties.indicator_value),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

function update_globals(properties) {
    min = properties.indicator_value_min;
    max = properties.indicator_value_max;
    indicator_name = properties.indicator_name;
}

function resetMapforRequest() {
    map.spin(true);
    if (map.hasLayer(geojson))
        map.removeLayer(geojson);
    try {
        map.removeControl(info);
    } catch (e) {}
    try {
        map.removeControl(legend);
    } catch (e) {}
    if (!map.hasLayer(base_layer))
        map.addLayer(base_layer);
}

function prepareMapWithResults(data) {
    update_globals(data.properties);

    geojson = L.geoJson(data, {
        style: styleFeature,
        onEachFeature: onEachFeature
    }).addTo(map);

    map.addControl(info);
    map.addControl(legend);
    if (map.hasLayer(base_layer))
        map.removeLayer(base_layer);
    map.spin(false);
}

function toggleSidebar(open) {
    if (open === true) {
        try {
            map.removeControl(sidebarBtn);
        } catch(e) {}
        sidebar.show();
    } else {
        sidebar.hide();
        map.addControl(sidebarBtn);
    }
}



function displayMap(mapID) {
    // base layer

    var options = {
        // center: L.LatLng(17.728, -6.724),
        // zoom: 6,
        dragging: false,
        touchZoom: false,
        scrollWheelZoom: false,
        doubleClickZoom: false,
        boxZoom: false,
        zoomControl: false,
        attributionControl: false
    };

    map = L.mapbox.map(mapID, null, options);

    base_layer = L.mapbox.tileLayer('http://tiles.sante.gov.ml/v2/mali-base.json').addTo(map);

    // health_areas_layer = L.mapbox.tileLayer('http://tiles.sante.gov.ml/v2/mali-health-areas.json');

    map.setView([13.448, -5.471], 7);

    // sidebar = L.control.sidebar('sidebar', {
    //     closeButton: true,
    //     position: 'right'
    // });

    info = L.control();
    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
    };

    // method that we will use to update the control based on feature properties passed
    info.update = function (props) {
        this._div.innerHTML = '<h4>'+ indicator_name +'</h4>' +  (props ?
            '<strong>' + props.name + ' : ' + props.indicator_value_human + '</strong>'
            : 'Déplacez la souris sur les zones.');
    };

    legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = getGrades(),
            labels = [],
            from, to;

        for (var i = 0; i < grades.length; i++) {
            from = grades[i];
            to = grades[i + 1];

            labels.push(
                '<i style="background:' + getColor(from + 1) + '"></i> ' +
                from + (to ? '&ndash;' + to : '+'));
        }

        div.innerHTML = labels.join('<br>');
        return div;
    };

    $('#update_map_btn').on('click', function (e) {
        e.preventDefault();
        var reporting_region = $("#health_region").attr('checked');
        var reporting_district = $("#health_district").attr('checked');
        var reporting_level = reporting_district == "checked" ? 'health_district' : 'health_region' ;
        var jsdata = JSON.stringify({
            project_slug: $("#project_slug").val(),
            level: reporting_level,
            display_hc: $("#display_hc").attr('checked'),
            // indicator_slug: "section1.NumberOfHealthUnitsWithin",
            // indicator_slug: "section1.NumberOfHealthUnitsInTime",
            indicator_slug: $('#section_select').val() + '.' + $('#indicator_select').val(),
            timing: $('#timing_select').val(),
            period_a: $('#period_a_select').val()
        });

        console.log(jsdata);

        resetMapforRequest();
        $.post("/api/indicators/geo", jsdata, function (data) {
            console.log("received JSON");
            console.log(data);
            prepareMapWithResults(data);
        });
    });

    // diam = S5C4
}