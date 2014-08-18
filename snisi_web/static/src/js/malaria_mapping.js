
Array.prototype.getUnique = function(){
   var u = {}, a = [];
   for(var i = 0, l = this.length; i < l; ++i){
      if(u.hasOwnProperty(this[i])) {
         continue;
      }
      a.push(this[i]);
      u[this[i]] = 1;
   }
   return a;
};

function QuantizeIndicatorScale() {

    QuantizeIndicatorScale.prototype.setup = function (manager, options) {

        var nb_breaks = manager.colors.length;
        if (manager.indicator_data_raw.length < nb_breaks) {
            nb_breaks = manager.indicator_data_raw.length;
        }

        this.scale = d3.scale.quantize()
            .domain([d3.min(manager.indicator_data_raw), d3.max(manager.indicator_data_raw)])
            .range(d3.range(nb_breaks).map(function(i) { return manager.colors[i]; }));
    };

    QuantizeIndicatorScale.prototype.boundaries_for_color = function (color) {
        return this.scale.invertExtent(color);
    };

    QuantizeIndicatorScale.prototype.color_for_value = function (data) {
        return this.scale(data);
    };

    QuantizeIndicatorScale.prototype.available_colors = function () {
        return this.scale.range();
    };

}

function FixedBoundariesScale(options) {

    this.options = options;

    FixedBoundariesScale.prototype.setup = function (manager) {
        this.colors = [];
        this.min = d3.min(manager.indicator_data_raw);
        this.max = d3.max(manager.indicator_data_raw);

        if (this.options.steps) {
            this.steps = this.options.steps;
            for (var i=0; i < this.steps.length; i++) {
                this.colors.push(manager.colors[i]);
            }
        } else {
            var nb_breaks = manager.colors.length;
            if (manager.indicator_data_raw.length < nb_breaks) {
                nb_breaks = manager.indicator_data_raw.length;
            }

            var step = this.max / nb_breaks;
            var steps = [];
            var current = this.min;
            steps.push(this.min);
            for (var j=0; j< nb_breaks; j++) {
                steps.push(current + step);
                this.colors.push(manager.colors[j]);
            }
            this.steps = steps;
        }
    };

    FixedBoundariesScale.prototype.boundaries_for_color = function (color) {
        var index = this.colors.indexOf(color);
        if (index + 1 >= this.steps.length && this.max > this.steps[index]) {
            upper_bound = this.max;
        } else {
            upper_bound = this.steps[index + 1];
        }

        if (index === 0 && this.min < this.steps[index]) {
            lower_bound = this.min;
        } else {
            lower_bound = this.steps[index];
        }
        return [lower_bound, upper_bound];
    };

    FixedBoundariesScale.prototype.color_for_value = function (data) {
        for (var i=this.steps.length - 1; i>=0; i--) {
            if (data >= this.steps[i]) {
                return this.colors[i];
            }
        }
        return this.colors[this.colors.length -1];
    };

    FixedBoundariesScale.prototype.available_colors = function () {
        return this.colors;
    };
}


function getMalariaMapManager(options) {

    function MalariaMapManager(options) {

        this.symbols = "abcdefghijklmnopqrstuvwxyz0123456789";
        this.color_is_missing = '#1d3f61'; // '#353f41';
        this.color_not_expected = '#737780'; //'#bfe1e6';
        this.color_regular_point = '#6f9bd1';
        this.color_yes = '#889f37'; //'#28ff00';
        this.color_no = '#4d2c74'; //'#ff1500';
        this.colors = options.colors || ["#fef0d9", "#fdcc8a", "#fc8d59", "#d7301f"];
        this.tiles_url_tmpl = 'http://{s}.tiles.sante.gov.ml/#SLUG#-#SUFFIX#/{z}/{x}/{y}.png';
        this.base_layer_url = 'http://{s}.tiles.sante.gov.ml/mali-base/{z}/{x}/{y}.png';
        this.marker_url_tmpl = 'http://tiles.sante.gov.ml/markers/#FILE#';
        this.initial_latitude = 14.0512;
        this.initial_longitude = -5.519499;
        this.initial_zoom = 8;
        this.mapID = options.mapID || "map";
        this.indicator_api_url = options.indicator_api_url || "/api/malaria/indicators";
        this.geojson_api_url = options.geojson_api_url || "/api/malaria/geojson";

        this.map = null; // Mapbox map object
        this.scale = null; // Mapbox scale control
        this.legend = null; // Mapbox on-map legend
        this.hc_legend = null; // Mapbox on-map legend for static matrix
        this.infobox = null; // Mapbox infobox control

        this.districts_layer = options.districts_layer || null; // Mapbox layer for districts
        this.hc_layer = options.hc_layer || null; // Mapbox layer for Health Centers

        this.indicator_scale = options.indicator_scale || new QuantizeIndicatorScale();

        this.title = options.title || null;
        this.subtitle = options.subtitle || null;

        // DOM elements of UI parts.
        this.map_title_e = null; // html title on top of map
        this.map_subtitle_e = null; // html sub title (date/entity)

        this.tabbar_e = null;
        this.district_select = null;
        this.indicator_section_select = null;
        this.indicator_select = null;
        this.year_select = null;
        this.month_select = null;

        this.getEmptyOption = function () {
            return $('<option value="-1">AUCUN</option>');
        };

        // Data that should be always accurate
        this.indicator_data = options.indicator_data || {};
        this.indicator_data_hc = options.indicator_data_hc || {};
        this.geodata = options.geodata || null;
        this.month = options.month || null; // 1-12 number of month selected
        this.month_name = options.month_name || null; // display-name of month
        this.year = options.year || null;

        this.indicators_list = options.indicators || {};
        this.current_region = options.current_region || null; // selected region slug
        this.current_district = options.current_district || null; // selected district slug
        this.current_indicator_section = null; // selected indicator section
        this.current_indicator = options.current_indicator || null; // selected indicator slug
        this.current_indicator_name = options.current_indicator_name || null; // selected indicator name

        this.static_map = options.static_map || false;

        this.load(options.load, options.onload);

    }

    MalariaMapManager.prototype.export_props = function() {
        return {
            title: this.title,
            subtitle: this.subtitle,
            current_region: this.current_region,
            current_district: this.current_district,
            current_indicator: this.current_indicator,
            current_indicator_name: this.current_indicator_name,
            year: this.year,
            month: this.month,
            month_name: this.month_name,
            geodata: this.geodata,
            indicator_data: this.indicator_data,
            indicator_data_hc: this.indicator_data_hc,
            indicator_scale: this.indicator_scale
            // districts_layer: this.districts_layer,
            // hc_layer: this.hc_layer
        };
    };

    MalariaMapManager.prototype._prepare_map = function() {
        // remove user interactions
        var options = {
            dragging: false,
            touchZoom: false,
            scrollWheelZoom: false,
            doubleClickZoom: false,
            boxZoom: false,
            zoomControl: false,
            attributionControl: false
        };

        if (this.static_map) {
            options.fadeAnimation = false;
            options.zoomAnimation = false;
            options.markerZoomAnimation = false;
        }

        this.map = L.mapbox.map(this.mapID, null, options);

        // background layer
        this.base_layer = L.tileLayer(this.base_layer_url)
                                  .addTo(this.map);

        // add a scale
        this.scale = L.control.scale({imperial:false})
                              .addTo(this.map);

        this.map.setView([this.initial_latitude, this.initial_longitude],
                         this.initial_zoom);

        this._prepare_map_legend();
        if (!this.static_map) {
            this._prepare_map_infobox();
        }
    };

    MalariaMapManager.prototype._prepare_map_legend = function () {
        var manager = this;

        this.legend = L.control({position: 'bottomright'});
        this.legend.onAdd = function (map) {
            this.div = L.DomUtil.create('div', 'info legend');
            this.update();
            return this.div;
        };
        this.legend.update = function() {

            var labels = [];

            function cleanNum(num) {
                return Math.round(num * 10) / 10;
            }

            $.each(manager.colors, function(index) {
                var color = manager.colors[index];
                var label = null;
                // boundaries = manager.indicator_scale.invertExtent(color);
                boundaries = manager.indicator_scale.boundaries_for_color(color);
                if (boundaries.length == 2 && !isNaN(boundaries[0]) && !isNaN(boundaries[1])) {
                    var from = boundaries[0];
                    var to = boundaries[1];

                    if (index !== 0) { from += 0.1; }

                    labels.push(
                        '<span><i style="background-color:' + color + '"></i> ' +
                        cleanNum(from) + ' – ' +
                        cleanNum(to) + '</span>');
                }
            });

            // SPACER
            if (labels.length) {
                labels.push('<span><i style="background-color:transparent"></i> </span>');
            }

            // NOT EXPECTED
            labels.push(
                '<span><i style="background-color:' + manager.color_not_expected +
                '"></i> <abbr title="Aucun rapport attendu pour cet ' +
                'indicateur">n/a</abbr></span>');

            // MISSING
            labels.push(
                '<span><i style="background-color:' + manager.color_is_missing +
                '"></i> <abbr title="Rapport manquant pour calculer cet ' +
                'indicateur">manquant</abbr></span>');

            this.div.innerHTML = labels.join('<br />');
        };
    };

    MalariaMapManager.prototype._prepare_map_hc_legend = function () {
        var manager = this;

        if (!this.static_map) {
            return;
        }

        this.hc_legend = L.control({position: 'topleft'});
        this.hc_legend.onAdd = function (map) {
            this.div = L.DomUtil.create('div', 'info hc_legend');
            this.update();
            return this.div;
        };
        this.hc_legend.update = function() {

            var labels = [];

            hc_lines = [];
            var l = manager.getCurrentDistrict().properties.children.features.length;
            for (var index=0; index<l; index++) {
                var feature = manager.getCurrentDistrict().properties.children.features[index];
                var slug = feature.properties.slug;
                if (feature !== null) {
                    var data = manager.getHCDataForSlug(slug).hdata;
                    // if (data == 1.replace('.00%', '%');
                    // var label = '<span class="hc_line">'+ feature.properties.name + ': ' + data +'</span>';
                    var label = '<span class="hc_line">'+ feature.properties['hc_legend_name'] +'</span>';
                    hc_lines.push(label);
                }
            }
            labels.push('<div class="hc_div">' + hc_lines.join('<br />') + '</div>');

            this.div.innerHTML = labels.join('<br />');
        };
    };

    MalariaMapManager.prototype._prepare_map_infobox = function () {
        var manager = this;
        this.infobox = L.control();
        this.infobox.onAdd = function (map) {
            this._div = L.DomUtil.create('div', 'info');
            this.update();
            return this._div;
        };
        this.infobox.update = function (feature) {
            if (feature === undefined) {
                this._div.innerHTML = 'Déplacez la souris sur les districts.';
                return;
            }
            var text, d = manager.getDataForSlug(feature.properties.slug);
            if (d === null || d === undefined)
                text = feature.properties.display_typed_name;
            else
                text = feature.properties.name + ' : ' + d.hdata;
            this._div.innerHTML = '<strong>' + text + '</strong>';
        };
        this._addInfoBox();
    };

    MalariaMapManager.prototype._prepareUI = function() {
        var manager = this;

        this.map_title_e = $('#map_title');
        this.map_subtitle_e = $('#map_subtitle');

        this.tabbar_e = $('#tab_bar');

        this.district_select = $('#health_district_select');
        this.district_select.on('change', function (event) {
            console.log("district select changed");
            var ds = manager.district_select.val();
            manager.current_district = (ds == '-1') ? null : ds;

            manager.parametersChanged();
        });

        this.indicator_select = $('#indicator_select');
        this.indicator_select.on('change', function (event) {
            console.log("indicator select changed");
            var is = manager.indicator_select.val();
            manager.current_indicator = (is == '-1') ? null : is;
            manager.current_indicator_name = (manager.current_indicator === null) ? "" :
            manager.indicator_select.children('option:selected').text();

            manager.parametersChanged();

            // switchIndicator
            // manager.loadIndicator();
        });

        this.indicator_section_select = $('#indicator_section_select');
        $.each(this.indicators_list, function (section_name) {
            var opt = $('<option />');
            opt.attr('value', section_name);
            opt.text(section_name);
            manager.indicator_section_select.append(opt);
        });
        this.indicator_section_select.on('change', function (event) {
            console.log("indicator section select changed");
            var iss = manager.indicator_section_select.val();
            manager.current_indicator_section = (iss == '-1') ? null : iss;

            // update indiciator list
            manager.indicator_select.empty();
            manager.indicator_select.append(manager.getEmptyOption());
            var list = manager.indicators_list[manager.current_indicator_section];
            $.each(list, function (index) {
                var opt = $('<option />');
                opt.attr('value', list[index].slug);
                opt.text(list[index].name);
                manager.indicator_select.append(opt);
            });
            manager.indicator_select.change();

            manager.parametersChanged();
        });
        this.indicator_section_select.change();

        this.year_select = $('#year_select');
        this.year_select.on('change', function (event) {
            console.log("year select changed");
            manager.year = manager.year_select.val();
            manager.parametersChanged();

            // switchIndicator
            manager.loadIndicator();
        });
        this.year_select.change();

        this.month_select = $('#month_select');
        this.month_select.on('change', function (event) {
            console.log("month select changed");
            manager.month = manager.month_select.val();
            manager.month_name = manager.month_select.children('option:selected').text();
            manager.parametersChanged();

            // switchIndicator
            manager.loadIndicator();
        });
        this.month_select.change();
    };

    MalariaMapManager.prototype._prepareTabBar = function() {
        if (this.geodata === null) {
            console.log("NO GEODATA. NO BAR");
            return;
        }

        var manager = this;

        this.tabbar_e.empty();
        $.each(this.geodata, function (region_slug){
            var region = manager.getRegion(region_slug);
            var link = $('<a/>');
            link.attr('href', '#');
            link.attr('slug', region.properties.slug);
            link.text(region.properties.name);
            manager.tabbar_e.append(link);
        });

        this.tabbar_e.children('a').on('click',
            function (event) {
                event.preventDefault();
                manager.switchRegion($(this).attr('slug'));
            }
        );
    };

    MalariaMapManager.prototype.updateTabBar = function () {
        var manager = this;
        this.tabbar_e.children('a').each(function (index) {
            $(this).removeClass('active');
            if ($(this).attr('slug') == manager.current_region) {
                $(this).addClass('active');
            }
        });
    };

    MalariaMapManager.prototype._updateDistrictSelect = function () {
        this.district_select.children("option[value="+ this.current_district +"]").attr('selected', 'selected');
    };

    MalariaMapManager.prototype._updateIndicatorSelect = function () {
        var indicator_val = this.current_indicator || '-1';
        this.indicator_select.children("option[value="+ indicator_val +"]").attr('selected', 'selected');
        var indicator_section_val = this.current_indicator_section || '-1';
        this.indicator_section_select.children("option[value='"+ indicator_section_val +"']").attr('selected', 'selected');
    };

    MalariaMapManager.prototype.parametersChanged = function() {
        if (!this.isReady()) {
            return;
        }
        this._updateTitle();

        this._updateDistrictSelect();

        if (this.isIndicator()) {
            this.loadIndicator();
        } else {
            this.switchRegion(this.current_region);
        }

    };

    MalariaMapManager.prototype.getCurrentRegion = function () {
        return this.getRegion(this.current_region);
    };

    MalariaMapManager.prototype.getRegion = function (region_slug) {
        return this.geodata[region_slug];
    };

    MalariaMapManager.prototype.getDistrict = function (district_slug) {
        var ret = null;
        var region = this.getCurrentRegion();
        $.each(region.features, function (index) {
            var feature = region.features[index];
            if (feature.properties.slug == district_slug) {
                ret = feature;
                return;
            }
        });
        return ret;
    };

    MalariaMapManager.prototype.getHCFeature = function (hc_slug) {
        var ret = null;
        var district = this.getCurrentDistrict();
        $.each(district.properties.children.features, function (index) {
            var feature = district.properties.children.features[index];
            if (feature.properties.slug == hc_slug) {
                ret = feature;
                return;
            }
        });
        return ret;
    };

    MalariaMapManager.prototype.getCurrentDistrict = function () {
        return this.getDistrict(this.current_district);
    };

    MalariaMapManager.prototype.isDistrict = function () {
        return this.current_district !== null;
    };

    MalariaMapManager.prototype.isIndicator = function () {
        return this.current_indicator !== null;
    };

    MalariaMapManager.prototype.isReady = function () {
        return this.geodata !== null;
    };

    MalariaMapManager.prototype.getCurrentFeature = function () {
        if (this.isDistrict()) {
            return this.getCurrentDistrict();
        }
        return this.getCurrentRegion();
    };

    MalariaMapManager.prototype._updateTitle = function () {

        var period_str, location_str, indicator_str, title, subtitle;

        if (this.isIndicator()) {
            title = this.current_indicator_name;
            period_str = this.month_name + " " + this.year;
            location_str = this.getCurrentFeature().properties.display_typed_name;
            subtitle = location_str + ", " + period_str;
        } else {
            title = this.getCurrentFeature().properties.display_typed_name;
            subtitle = null;
        }

        this.title = title;
        this.subtitle = subtitle;

        this.map_title_e.text(this.title || "");
        this.map_subtitle_e.text(this.subtitle || "");

    };

    MalariaMapManager.prototype.resetUI = function () {

        // update titles
        this._updateTitle();

        // update district list & selected
        var region = this.getCurrentRegion();
        this.district_select.empty();
        this.district_select.append(this.getEmptyOption());
        for (var i=0 ; i< region.features.length ; i++) {
            var opt = $('<option />');
            opt.attr('value', region.features[i].properties.slug);
            opt.text(region.features[i].properties.name);
            this.district_select.append(opt);
        }

        // update legend: remove ?
        if (!this.isIndicator()){
            this._removeLegend();
        } else {
            this._addLegend();
            this.legend.update();
        }

        // update infobox: remove ?


    };

    MalariaMapManager.prototype._addInfoBox = function () {
        try {
            this.map.addControl(this.infobox);
        } catch (e) {}
    };

    MalariaMapManager.prototype._removeInfoBox = function () {
        try {
            this.map.removeControl(this.infobox);
        } catch (e) {}
    };

    MalariaMapManager.prototype._addLegend = function () {
        try {
            this.map.addControl(this.legend);
        } catch (e) {}
    };

    MalariaMapManager.prototype._removeLegend = function () {
        try {
            this.map.removeControl(this.legend);
        } catch (e) {}
    };

    MalariaMapManager.prototype.startLoadingUI = function() {
        this.map.spin(true);
    };

    MalariaMapManager.prototype.stopLoadingUI = function() {
        this.map.spin(false);
    };

	MalariaMapManager.prototype.maxLengthHcName = function() {
        var max = 0;
        var manager = this;
        $.each(manager.getCurrentDistrict().properties.children.features, function (index) {
            var feature = manager.getCurrentDistrict().properties.children.features[index];
            var l = feature.properties.name.length;
            if (l > max) {
                max = l;
            }
        });
        return max;
    };

    MalariaMapManager.prototype.removeHCLayer = function() {
        if (this.map.hasLayer(this.hc_layer)) {
            this.map.removeLayer(this.hc_layer);
        }
        this.indicator_data_hc = {};
    };

    MalariaMapManager.prototype.resetAfterExport = function(data) {
        this.displayDistrictLayer(this.indicator_data);
        if (this.isDistrict()) {
            this.displayHCLayer(this.indicator_data_hc);
        }
    };

    MalariaMapManager.prototype.displayHCLayer = function(data) {
        console.log("displayHCLayer 2");
        this.removeHCLayer();

    	// remove region-level district names
    	this.removeLayer(this.region_names_layer);
    	this.removeLayer(this.region_borders_layer);
    	this.removeLayer(this.district_border);

        // display district names based on this district
        this.region_names_layer = this.getTileLayer(this.current_district, 'NAMES', true);
        this.region_borders_layer = this.getTileLayer(this.current_region, 'BORDERS', true);
        this.district_border = this.getTileLayer(this.current_district, 'BORDER', true);

        var manager = this;

        this.indicator_data_hc = data;


        function props_from_feature(feature) {
            var label = feature.properties.name;
            var color = manager.color_regular_point;
            var d = manager.getHCDataForSlug(feature.properties.slug);
            var yesno_istrue = false;
            if (d === undefined) {
            } else if (d.is_missing) {
                label += ': manquant';
                color = manager.color_is_missing;
            } else if (d.is_not_expected) {
                label += ': non attendu';
                color = manager.color_not_expected;
            } else {
                if (d.is_yesno) {
                    // change color of data point for YES/NO
                    yesno_istrue = d.data > 0;
                    color = yesno_istrue ? manager.color_yes : manager.color_no;
                    label += ': ';
                    label += yesno_istrue ? 'OUI' : 'NON';
                } else {
                    label += ': ' + d.hdata;
                }
            }
            return {label: label, color: color, data: d, yesno_istrue: yesno_istrue};
        }

        var maxNameLength = d3.max(manager.getCurrentDistrict().properties.children.features.map(function(feature){ return feature.properties.name.length;}));
        var maxDataLength = d3.max(manager.getCurrentDistrict().properties.children.features.map(function(feature){ return props_from_feature(feature).data.hdata.length;}));
        var maxTotalLength = maxNameLength + maxDataLength;
        $.each(manager.getCurrentDistrict().properties.children.features, function (index) {
            var feature = manager.getCurrentDistrict().properties.children.features[index];
            var props = props_from_feature(feature);
            var symbol = (index >= manager.symbols.length) ? 'hospital' : manager.symbols[index];
            feature.properties['title'] = props.label;
            var iconUrl = manager.marker_url_tmpl.replace('#FILE#', 'pin-m-'+symbol+'-'+manager.getColorName(props.color)+'.png');

            feature.properties['icon'] = {
            	'iconUrl': iconUrl,
            	'iconSize': [30, 70],
            	"iconAnchor": [25, 25],
            	"popupAnchor": [0, -25]
            }

            // feature.properties['marker-size'] = 'medium';
            // feature.properties['marker-color'] = props.color;
            // feature.properties['marker-symbol'] = symbol;

            var hc_legend_name = (symbol.length > 1) ? '+' : symbol.toUpperCase() + ". " + feature.properties.name;
            var nl = feature.properties.name.length + props.data.hdata.length;
            if (nl < maxTotalLength) {
                for (var i = nl ; i < maxTotalLength ; i++) {
                    hc_legend_name += " ";
                }
            }
            hc_legend_name += "  " + props.data.hdata;
            feature.properties['hc_legend_name'] = hc_legend_name;
            manager.getCurrentDistrict().properties.children.features[index] = feature;
        });

        manager.hc_layer = L.mapbox.featureLayer();

		manager.hc_layer.on('layeradd', function(e) {
            var marker = e.layer;
            var feature = marker.feature;
			marker.setIcon(L.icon(feature.properties.icon));
        });

        if (!manager.static_map) {
            manager.hc_layer.on('mouseover', function(e) {
                e.layer.openPopup();
            });
            manager.hc_layer.on('mouseout', function(e) {
                e.layer.closePopup();
            });
        }
        manager.hc_layer.setGeoJSON(manager.getCurrentDistrict().properties.children);
        manager.hc_layer.addTo(manager.map);
    };

    MalariaMapManager.prototype.displayDistrictLayer = function(data) {
        this.removeHCLayer();
        var manager = this;
        manager.removeDistrictLayer();
        manager.indicator_data = data;
        manager.indicator_data_raw = [];

        // remove region static
        manager.removeLayer(this.region_layer);
        manager.removeLayer(this.region_borders_layer);

        // quit if no data (display region STATIC)
        if (!Object.keys(manager.indicator_data).length) {
            this.region_layer = this.getTileLayer(this.current_region, 'STATIC', true);
            // add border layer for region
            this.region_borders_layer = this.getTileLayer(this.current_region, 'BORDERS', true);
            return;
        } else {
        	// remove region layers
            this.removeLayer(this.region_layer);
        }
        // remove region borders
        manager.removeLayer(manager.region_borders_layer);
        // remove district names
        manager.removeLayer(manager.region_names_layer);

        // collect actual data for indicator
        $.each(manager.indicator_data, function (index) {
            var d = manager.indicator_data[index];
            if (!d.is_missing && !d.is_not_expected) {
                manager.indicator_data_raw.push(d.data);
            }
        });
        manager.indicator_data_raw = manager.indicator_data_raw.getUnique();
        manager.indicator_scale.setup(manager);
        
        // build all layers for districts
        manager.districts_layers = {};
        var getKey = function (feature, id) {
            return feature.properties.slug + '-' + id;
        };

        // var borderLayers = [];
        $.each(manager.getCurrentRegion().features, function (index) {
            var feature = manager.getCurrentRegion().features[index];
            var color = manager.getColorFor(manager.getDataForSlug(feature.properties.slug), true);
            var tileUrl = manager.getTileUrl(feature.properties.slug, manager.getColorName(color));
            // var tileBorderUrl = manager.getTileUrl(feature.properties.slug, 'BORDER');
            // var tileNamesUrl = manager.getTileUrl(feature.properties.slug, 'NAMES');

            manager.districts_layers[getKey(feature, 'shape')] = L.tileLayer(tileUrl, {opacity: manager.tileOpacity}).addTo(manager.map);
        });

        // add region district names if on a static map and not a district
        if (manager.static_map && !manager.isDistrict()) {
            //L.tileLayer(manager.getTileUrl(manager.getCurrentRegion(), 'NAMES')).addTo(manager.map);
        }

        manager.districts_layer = L.geoJson(manager.getCurrentRegion(), {
            style: function (feature) { return {fillOpacity: 0, opacity: 0}; },
            onEachFeature: function(feature, layer) {

                if (manager.static_map) {
                    if (manager.isDistrict() && feature.properties.slug == manager.current_district) {
                        // add
                        // manager.districts_layers[getKey(feature, 'names')].setOpacity(1);

                        // add border layer
                        // manager.districts_layers[getKey(feature, 'border')].setOpacity(1);
                    }
                    return;
                }

                layer.on('mouseover', function(event) {
                    var layer = event.target;
                    manager.infobox.update(layer.feature);

                    // switch border opacity ON
                    // manager.districts_layers[getKey(layer.feature, 'border')].setOpacity(1);
                    manager.districts_layers[feature.properties.slug+'-shape'].setOpacity(1);


                    if (!L.Browser.ie && !L.Browser.opera) {
                        if (manager.isDistrict()) {
                            try {
                                manager.hc_layer.bringToFront();
                            } catch (e) {}
                        }
                    }
                });

                layer.on('mouseout', function(event) {
                    // swicth border off
                    //manager.districts_layers[getKey(layer.feature, 'border')].setOpacity(0);

                    manager.districts_layers[feature.properties.slug+'-shape'].setOpacity(manager.tileOpacity);

                    if (!manager.isDistrict()) {
                        manager.infobox.update();
                    }
                });

                layer.on('click', function (e) {
                    manager.current_district = e.target.feature.properties.slug;
                    manager.parametersChanged();
                });

            }
        });

        manager.map.addLayer(manager.districts_layer);
        manager._addLegend();

        // we need to add region borders back
        this.region_borders_layer = this.getTileLayer(this.current_region, 'BORDERS', true);
        // as well as district names if not on a district
        if (!manager.isDistrict()) {
        	this.region_names_layer = this.getTileLayer(this.current_region, 'NAMES', true);
        }

    };

    MalariaMapManager.prototype.getTileLayer = function (feature_slug, suffix, add_to_map) {
    	var burl = this.getTileUrl(feature_slug, suffix);
    	var payload = {};
		$.ajax(burl.replace('{}.', '').replace('{z}/{x}/{y}.png', 'metadata.json'), {async:false, }).success(function (data){
			try {
				var bs = data['bounds'].split(',');
				var southWest = L.latLng(parseFloat(bs[1]), parseFloat(bs[0])),
	    			northEast = L.latLng(parseFloat(bs[3]), parseFloat(bs[2])),
	    			bounds = L.latLngBounds(southWest, northEast);
	    	} catch (e) { console.log(e.toString()); console.log(data); var bounds = null; }
			payload = {
    			"bounds": bounds,
    			"minZoom": parseInt(data['minzoom']),
    			"maxZoom": parseInt(data['maxzoom']),
			};
    	});

		// this.getTileUrl(feature_slug, suffix);
    	var l = L.tileLayer(burl, payload);
    	if (add_to_map) {
    		l.addTo(this.map);
    	}
    	return l;
	};

    MalariaMapManager.prototype.getTileUrl = function (feature_slug, suffix) {
        return this.tiles_url_tmpl.replace('#SLUG#', feature_slug).replace('#SUFFIX#', suffix);
    };

    MalariaMapManager.prototype.removeLayer = function(layer) {
    	if (this.map.hasLayer(layer)) {
    		this.map.removeLayer(layer);
    	}

    };

    MalariaMapManager.prototype.removeDistrictLayer = function() {
        this.indicator_data = {};
        this._removeLegend();
        
        this.removeLayer(this.districts_layer);
    	this.removeLayer(this.district_border);
    	this.removeLayer(this.region_names_layer);

    	if (this.districts_layers) {
    		var manager = this;
	        $.each(this.districts_layers, function (index, layer) {
	        	manager.removeLayer(layer);
	        });
	    }
    };

    MalariaMapManager.prototype.loadIndicator = function() {
        // probably just a parameter change (month/year)
        if (!this.isIndicator()) {
            return;
        }

        var region = this.current_region;

        var jsdata = JSON.stringify({
            entity_slug: this.getCurrentFeature().properties.slug,
            indicator_slug: this.current_indicator,
            year: this.year,
            month: this.month
        });

        this.startLoadingUI();
        var manager = this;
        $.post(this.indicator_api_url, jsdata, function (data) {
            try {
                if (manager.isDistrict()) {
                    manager.displayHCLayer(data);
                } else {
                    manager.removeHCLayer();
                    manager.displayDistrictLayer(data);
                }

                manager.updateZoom();
                manager.stopLoadingUI();
            } catch (exp) {
                console.log("catched expection");
                console.log(exp);
                manager.switchRegion(region);
            }

        }).fail(function () {
            console.log("failed JSON");
            manager.stopLoadingUI();
            manager.switchRegion(region);
        });
    };

    MalariaMapManager.prototype.removeLayer = function(layer) {
        if (this.map.hasLayer(layer)) {
            this.map.removeLayer(layer);
        }
    };

    MalariaMapManager.prototype.zoomTo = function (layer) {
        if (!layer)
        	return;
        try {
        	var bounds = layer.getBounds();
        } catch (e) {
        	try {
        		var bounds = layer.options.bounds;
        	} catch (ee) {
        		return;
        	}
        }
        this.map.fitBounds(bounds);
    };

    MalariaMapManager.prototype.getDistrictLayer = function (district_slug) {
        var layer = null;
        var manager = this;
        $.each(this.map._layers, function (index) {
            var l = manager.map._layers[index];
            try {
                if (l.feature.properties.slug == district_slug)
                    layer = l;
            } catch(e) {}
        });
        return layer;
    };

    MalariaMapManager.prototype.updateZoom = function () {
        var layer;
        if (this.isDistrict()) {
            layer = this.getDistrictLayer(this.current_district);
        } else {
        	// we're at region static
        	if (this.map.hasLayer(this.region_layer)) {
        		layer = this.region_layer;
        	} else {
            	layer = this.districts_layer;
            }
        }
        this.zoomTo(layer);
    };

    MalariaMapManager.prototype.switchRegion = function(region_slug) {
        console.log("switching to region " + region_slug);
        this.current_region = region_slug;
        this.current_district = null;
        this.current_indicator = null;
        this.current_indicator_name = null;

        this._updateTitle();
        this.infobox.update();
        this._updateIndicatorSelect();
        this.removeHCLayer();

        // make sure UI is clean
        this.removeDistrictLayer();
        try {
            this.updateTabBar();
            this.resetUI();
        } catch(exp){}

        if (this.isIndicator()) {
            this.loadIndicator();
        } else {
            // this.districts_layer = L.geoJson(this.getCurrentRegion(), {
            //     style: this.noIndicatorStyle
            // });
            // this.map.addLayer(this.districts_layer);
            this.displayDistrictLayer({});
        }
        this.updateZoom();
    };


    MalariaMapManager.prototype.prepare = function() {
        this._prepare_map();
        if (!this.static_map) {
            this._prepareUI();
        }
    };

    MalariaMapManager.prototype.loadStaticMap = function(callback) {

        // add legend
        this._addLegend();
        if (this.isDistrict()) {
            this._prepare_map_hc_legend();
            this.map.addControl(this.hc_legend);
        }

        var indicator_data_hc = this.indicator_data_hc;

        // display the layers we have
        if (this.indicator_data) {
            this.displayDistrictLayer(this.indicator_data);
        }

        // display HC layer
        if (this.isDistrict() && Object.keys(indicator_data_hc).length) {
            this.displayHCLayer(indicator_data_hc);
        }

        // zoom to current feature
        this.updateZoom();

        if (callback !== undefined) {
            callback(this);
        }
    };

    MalariaMapManager.prototype.loadGeoData = function(callback) {
        var manager = this;
        $.get(this.geojson_api_url, {},
            function (data) {
                console.log("received region GeoJSON");
                // saved geodata as it contains all our polygons & points
                manager.geodata = data;

                // display the region tab bar.
                manager._prepareTabBar();

                // display default region
                manager.switchRegion("2732");

                // launch callback
                if (callback !== undefined) {
                    callback(this);
                }
            }
        );
    };

    MalariaMapManager.prototype.load = function(loadData, callback) {
        this.prepare();
        if (loadData === true) {
            this.loadGeoData(callback);
        }
        if (this.static_map === true) {
            this.loadStaticMap(callback);
        }
    };

    MalariaMapManager.prototype.getDataForSlug = function(slug) {
        return this.indicator_data[slug];
    };

    MalariaMapManager.prototype.getHCDataForSlug = function(slug) {
        return this.indicator_data_hc[slug];
    };

    MalariaMapManager.prototype.getColorFor = function(data) {

        if (data === undefined)
            return this.color_is_missing;
        if (data.is_not_expected) {
            return this.color_not_expected;
        }
        if (data.is_missing) {
            return this.color_is_missing;
        }
        // var color = this.indicator_scale(data.data);
        var color = this.indicator_scale.color_for_value(data.data);
        // if (color === undefined && this.indicator_scale.range().length == 1) {
        if (color === undefined && this.indicator_scale.available_colors().length == 1) {
            color = this.colors[0];
        }
        return color;
    };

    MalariaMapManager.prototype.getColorName = function(color) {
    	index = this.colors.indexOf(color);
    	if (index == -1) {
    		if (color == this.color_is_missing) {
    			return 'MISSING';
    		}
    		if (color == this.color_not_expected) {
    			return 'NOT_EXPECTED';
    		}
    		if (color == this.color_regular_point) {
    			return 'REGULAR';
    		}
    		if (color == this.color_yes) {
    			return 'YES';
    		}
    		if (color == this.color_no) {
    			return 'NO';
    		}
    	} else {
    		return index;
    	}
    };

    MalariaMapManager.prototype.noIndicatorStyle = function (feature) {
        return {
            fillColor: "#6f9bd1",
            weight: 2,
            opacity: 1,
            color: 'white',
            fillOpacity: 1};
    };

    return new MalariaMapManager(options);
}


function roundRect(ctx, x, y, width, height, radius, fill, stroke) {
  if (typeof stroke == "undefined" ) {
    stroke = true;
  }
  if (typeof radius === "undefined") {
    radius = 5;
  }
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
  if (stroke) {
    ctx.stroke();
  }
  if (fill) {
    ctx.fill();
  }
}


function getMapExporter(options) {

    function MapExporter (options) {
        this.buttonID = options.buttonID || "export_map_btn";
        this.button = $('#' + this.buttonID);
        this.mapID = options.mapID || "exported_map";
        this.mapManager = options.mapManager;
        this.auto_click = options.auto_click || false;
        this.exportedMapManager = null;
        this.timer = null;

        this.registerButton();
    }

    MapExporter.prototype.removeTimeout = function () {
        clearTimeout(this.timer);
    };

    MapExporter.prototype.registerButton = function() {
        var manager = this;
        this.button.on('click', function (e) {
            e.preventDefault();

            if ($('html').is('.ie6, .ie7, .ie8, .ie9')) {
                alert("ATTENTION!\nL'export de la cartographie n'est pas " +
                      "possible avec Internet Explorer 9 et plus ancien.\n" +
                      "Merci d'utiliser une version plus récente d'Internet " +
                      "Explorer ou un autre navigateur tel Mozilla Firefox " +
                      "ou Google Chrome.");
                return;
            }

            // make sure we launch it only once until it finishes.
            var state = $(this).attr('disabled');
            // var timer;
            var cancel = function() {
                console.log("cancelled.");
                manager.removeTimeout();
                manager.resetButton();
                manager.restoreButton();
            };
            if (state != 'disabled') {
                try {
                    manager.timer = setTimeout(cancel, 90000);
                    manager.do_export();
                } catch(exp) {
                    console.log("Error while exporting.");
                    console.log(exp.toString());
                    cancel();
                }
            }
        });
        this.restoreButton();
    };

    MapExporter.prototype.makeButtonPending = function () {
        this.button.html('<i class="fa fa-spinner faa-spin animated"></i> en cours…');
        this.button.attr('disabled', 'disabled');
    };

    MapExporter.prototype.restoreButton = function () {
        this.button.text('Exporter');
        this.button.removeAttr('disabled');
    };

    MapExporter.prototype.resetButton = function () {
        $('.exportbuttons .save-as-png').remove();
        $('#' + this.mapID).remove();
        $('.map-holder').append('<div id="exported_map" />');
    };

    MapExporter.prototype.do_export = function() {
        console.log("Exporting map…");

        // reset button state
        this.resetButton();
        this.makeButtonPending();

        // prepare static map options
        var options = this.mapManager.export_props();
        options.static_map = true;
        options.mapID = this.mapID;

        var manager = this;
        options.onload = function (mmap) {

            function cssvalue(elem, prop) {
                return parseInt(elem.css(prop).replace('px', ''));
            }

            var map = mmap.map;
            doImage = function (err, canvas) {
                var titleSizePx = 22;
                var titleHeight = titleSizePx + Math.round(titleSizePx * 0.25);
                var subtitleSizePx = 16;
                var subtitleHeight = subtitleSizePx + Math.round(subtitleSizePx * 0.25);
                var subtitleHeightPosition = (titleHeight + (subtitleHeight - (titleSizePx / 2)));
                var textHeight = titleHeight;
                if (manager.mapManager.subtitle) {
                    textHeight += subtitleHeight;
                }

                var new_can = $('#canvas')[0];
                new_can.width = canvas.width;
                new_can.height = canvas.height + textHeight;
                var canvasWidth = new_can.width;
                var canvasHeight = new_can.height;
                var ctx = new_can.getContext("2d");
                // fill with white
                ctx.fillStyle = "rgb(255,255,255)";
                ctx.fillRect(0, 0, new_can.width, new_can.height);
                ctx.drawImage(canvas, 0, textHeight);

                // draw title
                ctx.fillStyle = "black";
                ctx.font = titleSizePx + "px 'Droid Sans',sans-serif";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";

                // draw subtitle
                ctx.fillText(manager.mapManager.title, new_can.width / 2 , (titleHeight - (titleSizePx / 2)));
                if (manager.mapManager.subtitle !== null) {
                    ctx.font = subtitleSizePx + "px 'Droid Sans',sans-serif";
                    ctx.fillText(manager.mapManager.subtitle, new_can.width / 2 , subtitleHeightPosition);
                }

                // draw scale
                var leafletScaleWidth = parseInt($('#'+ manager.mapID +' .leaflet-control-scale-line').css('width').replace('px', ''));
                var scaleHeight = 16;
                var scaleWidth = leafletScaleWidth; // 74
                var scaleLeft = 10;
                var scaleBottom = new_can.height - 10;
                var scaleColor = "#333333";
                // draw white .5 opacity rect
                ctx.fillStyle = "rgba(255,255,255, 0.5)";
                ctx.fillRect(scaleLeft, scaleBottom - scaleHeight,
                             scaleWidth, scaleHeight);
                // draw border
                ctx.strokeStyle = scaleColor;
                ctx.lineWidth = 2;
                ctx.lineJoin = 'round';
                ctx.lineCap = 'round';
                ctx.beginPath();
                ctx.moveTo(scaleLeft, scaleBottom - scaleHeight);
                ctx.lineTo(scaleLeft, scaleBottom);
                ctx.lineTo(scaleLeft + scaleWidth, scaleBottom);
                ctx.lineTo(scaleLeft + scaleWidth, scaleBottom - scaleHeight);
                ctx.stroke();
                // draw text
                var scale_text = $('#'+ manager.mapID +' .leaflet-control-scale-line').text();
                ctx.fillStyle = scaleColor;
                ctx.font = "11px 'Droid Sans',sans-serif";
                ctx.textAlign = "left";
                ctx.textBaseline = "bottom";
                ctx.fillText(scale_text, scaleLeft + 2, scaleBottom - 1);

                // draw legend
                var html_legend = $('#' + manager.mapID + ' .legend');
                if (html_legend.length) {
                    var legendWidth = cssvalue(html_legend, 'width');
                    var legendHeight = cssvalue(html_legend, 'height');
                    var legendMarginRight = cssvalue(html_legend, 'margin-right');
                    var legendMarginBottom = cssvalue(html_legend, 'margin-bottom');
                    var legendPaddingLeft = cssvalue(html_legend, 'padding-left');
                    var legendPaddingTop = cssvalue(html_legend, 'padding-top');
                    var legendX = canvasWidth - legendWidth - legendMarginRight;
                    var legendY = canvasHeight - legendHeight - legendMarginBottom;
                    ctx.fillStyle = "rgba(255,255,255, 0.8)";
                    ctx.strokeStyle = '#bbbbbb';
                    roundRect(ctx, legendX, legendY,
                              legendWidth, legendHeight, 5, true, true);
                    // draw legend text
                    ctx.shadowOffsetX = 0;
                    ctx.shadowOffsetY = 0;
                    ctx.shadowBlur = 0;
                    var legendTextX = legendX + legendPaddingLeft;
                    var legendTextY = legendY + legendPaddingTop;
                    var currentLegendTextY = legendTextY;
                    html_legend.children('span').each(function (index, spanElem) {
                        var span = $(spanElem);
                        var i = span.children('i');
                        var width = cssvalue(i, 'width');
                        var height = cssvalue(i, 'height');
                        var text = span.text();
                        ctx.fillStyle = i.css('background-color');
                        ctx.fillRect(legendTextX, currentLegendTextY,
                                      width, height);
                        // text
                        ctx.fillStyle = scaleColor;
                        ctx.font = "12px 'Droid Sans',sans-serif";
                        ctx.textAlign = "left";
                        ctx.textBaseline = "middle";
                        ctx.fillText(text,
                                     legendTextX + width,
                                     currentLegendTextY + height / 2);
                        currentLegendTextY += height;
                    });
                }

                // draw HC legend
                var html_hc_legend = $('#' + manager.mapID + ' .hc_legend');
                if (html_hc_legend.length) {
                    var hcLegendWidth = cssvalue(html_hc_legend, 'width');
                    var hcLegendHeight = cssvalue(html_hc_legend, 'height');
                    var hcLegendMarginLeft = cssvalue(html_hc_legend, 'margin-left');
                    var hcLegendMarginTop = cssvalue(html_hc_legend, 'margin-top');
                    var hcLegendPaddingLeft = cssvalue(html_hc_legend, 'padding-left');
                    var hcLegendPaddingTop = cssvalue(html_hc_legend, 'padding-top');
                    var hcLegendX = hcLegendMarginLeft;
                    var hcLegendY = hcLegendMarginTop + textHeight;
                    ctx.strokeStyle = '#bbbbbb';
                    ctx.fillStyle = "rgba(255,255,255, 0.8)";
                    ctx.shadowOffsetX = 0;
                    ctx.shadowOffsetY = 0;
                    ctx.shadowBlur = 0;
                    ctx.shadowColor = scaleColor;
                    roundRect(ctx, hcLegendX, hcLegendY,
                              hcLegendWidth, hcLegendHeight, 5, true, true);
                    var currentHcLegendTextY = hcLegendY + hcLegendPaddingTop;
                    var oddColor = "rgba(33,33,33, 0.1)";
                    var evenColor = "rgba(255,255,255, 0.8)";
                    $('.hc_line').each(function (index, spanElem) {
                        var span = $(spanElem);
                        var width = cssvalue(span, 'width');
                        var height = 10; //cssvalue(span, 'height');
                        height -= 1;
                        var text = span.text();
                        // text
                        ctx.fillStyle = (index % 2 === 0) ? null : oddColor;
                        if (index % 2 !== 0) {
                            ctx.fillRect(hcLegendX, currentHcLegendTextY,
                                          hcLegendWidth, height);
                        }
                        ctx.fillStyle = scaleColor;
                        ctx.font = "9px droid_sans_monoregular";
                        ctx.textAlign = "left";
                        ctx.textBaseline = "middle";
                        ctx.fillText(text,
                                     hcLegendX + hcLegendPaddingLeft,
                                     currentHcLegendTextY + height / 2);
                        currentHcLegendTextY += height;
                    });
                }

                console.log("done doImage");

                var url = new_can.toDataURL();
                var link = $('<a />');
                link.attr('href', url);
                link.attr('download', 'exported_map.png');
                link.attr('class', 'save-as-png pure-button');
                link.html('<i class="fa fa-save"></i>');
                link.attr('title', "Enregistrer l'image PNG");
                $('.exportbuttons').append(link);

                // remove map
                $('#' + manager.mapID).remove();

                // toggle back
                manager.restoreButton();

                // emulate a click on the created button to popup save dialog
                if (manager.auto_click === true) {
                    var e = document.createEvent("MouseEvents");
                    e.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0,
                                     false, false, false, false, 0, null);
                    link[0].dispatchEvent(e);
                }

                manager.removeTimeout();
            };

            // wait 2s between map creation and exporting to canvas
            // to allow any animation to complete
            var interval;
            interval = setInterval(function (){
                clearInterval(interval);
                leafletImage(map, doImage);
            }, 2000);

        };
        this.exportedMapManager = getMalariaMapManager(options);

    };
    return new MapExporter(options);
}
