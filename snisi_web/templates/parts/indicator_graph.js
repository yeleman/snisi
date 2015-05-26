{% load snisi %}
{% load l10n %}
var PERCENT = "";
hc_graphs.push({
    chart: {
        renderTo: 'widget_{{ id }}', defaultSeriesType: '{{ table.graph_type }}', backgroundColor: '#ebebeb'
    },
    colors: [{% for color in table.colors%}'{{ color }}',{% endfor %}],
    legend: {},
    title: {text: null},
    xAxis: {
        type: 'datetime',
        maxZoom: 84600 * 1000,
        dateTimeLabelFormats: {
            millisecond: '%H:%M:%S.%L',
            second: '%H:%M:%S',
            minute: '%H:%M',
            hour: '%H:%M',
            day: '%e. %b',
            week: '%e. %b',
            month: '{% if table.periods|length < 6 %}%B %Y{% else %}%b %y{% endif %}',
            year: '%Y'
        },
        labels: {
            {% if table.rotate_labels %}rotation: -90,{% endif %}
        }
    },
    {% if table.multiple_axis %}
    yAxis: [
    	{% for axe in table.multiple_axis %}
    	{
	    	title: {text: null},
	        min:0,
	        {% if axe.show_as_percentage %}max:100, show_as_percentage: true,{% endif %}
	        {% if axe.opposite %}opposite: true,{% endif %}
	        labels: {
	        	{% if axe.show_as_percentage %}
	        	formatter: function () { return this.value + '%'; }
	        	{% endif %}
        	}
	    },
	    {% endfor %}
    ],
    {% else %}
    yAxis: {
        title: {text: null},
        min:0,
        {% if table.show_as_percentage %}
        max:100,
        show_as_percentage: true,
        {% endif %}
        labels: {
        	{% if table.show_as_percentage %}
        	formatter: function () { return this.value + '%'; }
        	{% endif %}
    	}
    },
    {% endif %}
    series: [
        {% for line in table.render_for_graph %}
        {
            name: "{{ line.label|safe }}",
            yAxis: {{ line.yAxis }},
            type: "{{ line.graph_type }}",
            data: {% localize off %}[{% for p, data in line.data %}[{{ p.start_on|to_jstimestamp }}, {{ data|default_if_none:"null" }}],{% endfor %}]{% endlocalize %}
        },
        {% endfor %}
    ],
    tooltip: {
    	enabled: false,
        formatter: function() {
        	if (this.y != null) {
        		var nf = (Math.round(this.y * 10) / 10).toString().replace('.', ',');
        		if (this.series.yAxis.userOptions.show_as_percentage) {
        			return nf + '%';
        		}
        		return  nf;
        	}
        }
    },
    plotOptions: {
        line: {
            animation: false,
            dataLabels: {
                enabled: true,
            },
            enableMouseTracking: false
        },
        column: {
            animation: false,
            enableMouseTracking: false,
            {% if table.graph_stacking %}
            stacking: 'percent',
            {% endif %}
        },
        series: {
        	dataLabels: {
                color: 'black',
                enabled: true,
                formatter: function () {
                	if (this.y != null) {
                		var nf = (Math.round(this.y * 10) / 10).toString().replace('.', ',');
                		if (this.series.yAxis.userOptions.show_as_percentage) {
                			return nf + '%';
                		}
                		return  nf;
                	}
        		},
            },
        }
    },
    exporting: {
        enabled: true,
    },
    credits: {
        enabled: true,
        text: "© SNISI – {{ table.last_period }}",
        href: null
    },
});
