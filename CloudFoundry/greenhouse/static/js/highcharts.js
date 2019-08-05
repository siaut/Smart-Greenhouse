var chart;
var chart2;
var chart3;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[0].addPoint(point, true, shift);

            // call it again after one second
            setTimeout(requestData, 5000);
        },
        cache: false
    });
}

function requestData2() {
    $.ajax({
        url: '/live-data2',
        success: function(point) {
            var series = chart2.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart2.series[0].addPoint(point, true, shift);

            // call it again after one second
            setTimeout(requestData2, 5000);
        },
        cache: false
    });
}

function requestData3() {
    $.ajax({
        url: '/live-data3',
        success: function(point) {
            var series = chart3.series[0],
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart3.series[0].addPoint(point, true, shift);

            // call it again after one second
            setTimeout(requestData3, 5000);
        },
        cache: false
    });
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'spline',
			animation: Highcharts.svg, // don't animate in old IE
			marginRight: 10,
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Light'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            
            title: {
                text: 'Light'
            }
        },
        series: [{
            name: 'Light Sensor',
            data: []
        }]
    });

//==============================
	chart2 = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container2',
            defaultSeriesType: 'spline',
			animation: Highcharts.svg, // don't animate in old IE
			marginRight: 10,
            events: {
                load: requestData2
            }
        },
        title: {
            text: 'Temperature'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: 'Temperature'
            }
        },
        series: [{
            name: 'Temperature Sensor',
            data: []
        }]
    });



chart3 = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container3',
            defaultSeriesType: 'spline',
			animation: Highcharts.svg, // don't animate in old IE
			marginRight: 10,
            events: {
                load: requestData3
            }
        },
        title: {
            text: 'Soil Moisture'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: 'Soil Moisture'
            }
        },
        series: [{
            name: 'Soil Moisture Sensor',
            data: []
        }]
    });
//====================================
});