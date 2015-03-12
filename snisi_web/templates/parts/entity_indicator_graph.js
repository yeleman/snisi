{% load snisi %}
{% load l10n %}
var PERCENT = "";
hc_graphs.push({
    chart: {
        renderTo: 'widget_{{ id }}', defaultSeriesType: '{{ table.graph_type }}', backgroundColor: '#ebebeb'
    },
    colors: [
       '#4572A7',
       '#AA4643',
       '#89A54E',
       '#80699B',
       '#3D96AE',
       '#DB843D',
       '#92A8CD',
       '#A47D7C',
       '#B5CA92'
    ],
    legend: {},
    title: {text: null},
    xAxis: {
    	categories: [
    		{% for entity in table.entities %}
    		"{{ entity.name }}",
    		{% endfor %}
        ],
        labels: {
            {% if table.rotate_labels %}rotation: -90,{% endif %}
        }
    },
    yAxis: {
        title: {text: null},
        min:0,
        {% if table.show_as_percentage %}
        max:100,
        {% endif %}
    },
    series: [
        {% for line in table.render_for_graph %}
        {
            name: "{{ line.label|safe }}",
            data: {% localize off %}[{% for entity, data in line.data %}{{ data|default_if_none:"null" }},{% endfor %}]{% endlocalize %}
        },
        {% endfor %}
    ],
    tooltip: {
        {% if table.show_as_percentage %}
        formatter: function () { return this.series.name + ' : ' + (Math.round(this.y * 10) / 10).toString().replace('.', ',') + '%'; }
        {% endif %}
    },
    plotOptions: {
        line: {
            animation: false,
            dataLabels: {
                enabled: true
            },
            enableMouseTracking: false
        },
        column: {
            animation: false,
            enableMouseTracking: false,
            {% if table.graph_stacking %}
            stacking: 'percent',
            {% endif %}
            dataLabels: {
                color: 'black',
                enabled: true,
                {% if table.show_as_percentage %}
                formatter: function () { if (this.y != null) {return (Math.round(this.y * 10) / 10).toString().replace('.', ',') + '%';} }
                {% endif %}
            },
        },
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
