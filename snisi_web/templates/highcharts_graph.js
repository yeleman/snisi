{% load snisi %}
{% load l10n %}
{
    chart: {
        renderTo: 'widget_{{ id }}',
        defaultSeriesType: '{{ table.graph_type }}',
        backgroundColor: '#ebebeb'
    },
    lang: {
        months: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
        weekdays: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
        decimalPoint: ",",
        downloadPNG: "Exporter en PNG",
        drillUpText: "Revenir à {series.name}.",
        loading: "Chargement…",
        printChart: "Imprimer",
        numericSymbols: [null, null, null, null, null, null],
        resetZoom: "Restaurer niveau de zoom.",
        resetZoomTitle: "Restaurer le niveau de zoom 1:1.",
        shortMonths: [ "Jan" , "Fév" , "Mar" , "Avr" , "Mai" , "Jui" , "Juil" , "Aôu" , "Sep" , "Oct" , "Nov" , "Déc"],
        thousandsSep: " ",
        contextButtonTitle: "Menu contextuel"
    },
    colors: [{% for color in table.colors%}'{{ color }}',{% endfor %}],
    legend: {},
    title: {text: null},
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: {
            millisecond: '%H:%M:%S.%L',
            second: '%H:%M:%S',
            minute: '%H:%M',
            hour: '%H:%M',
            day: '%e. %b',
            week: '%e. %b',
            month: '{% if table.periods|length < 6 %}%B %Y{% else %}%b %y{% endif %}',
            year: '%Y'
        }
    },
    {% if table.dual_axis %}
    yAxis: [
        {
            labels: {
                {% if table.dual_axis.default.format %}
                format: '{{ table.dual_axis.default.format }}',
                {% endif %}
            },
            title: {
                text: '{{ table.dual_axis.default.label }}',
            }
        },
        {
            labels: {
                {% if table.dual_axis.opposite.format %}
                format: '{{ table.dual_axis.opposite.format }}',
                {% endif %}
            },
            title: {
                text: '{{ table.dual_axis.opposite.label }}',
            },
            opposite: true
        },
    ],
    {% else %}
    yAxis: {
        title: {text: null},
        min:0,
        {% if table.as_percentage %}
        max:100,
        {% endif %}
    },
    {% endif %}
    series: [
        {% for line in table.render_for_graph %}
        {
            {% if table.dual_axis %}
            yAxis: {{ forloop.counter0 }},
            {% endif %}
            name: '{{ line.label }}',
            data: {% localize off %}[{% for p, data in line.data %}[{{ p.start_on|to_jstimestamp }}, {{ data|default_if_none:"null" }}],{% endfor %}]{% endlocalize %}
        },
        {% endfor %}
    ],
    tooltip: {
        {% if table.as_percentage %}
        formatter: function () { return this.series.name + ' : ' + (Math.round(this.y * 10) / 10).toString().replace('.', ',') + '%'; }
        {% endif %}
        // formatter: function() { return ''+ this.series.name +': '+ this.y +PERCENT;}
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
            dataLabels: {
                color: 'black',
                enabled: true,
                {% if table.as_percentage %}formatter: function () { return (Math.round(this.y * 10) / 10).toString().replace('.', ',') + '%'; },{% endif %}
                {% if table.rotate_labels %}rotation: -90,{% endif %}
            }
        }
    },
    exporting: {
        enabled: true,
    },
    credits: {
        enabled: true,
        text: "© PNLP – {{ table.last_period }}",
        href: null
    },
}
