function drawGraph(graph_div, metrics, unit, _min, _max) {
  old_plot_data = $.data($(graph_div)[0], 'plot');
  if (typeof old_plot_data != "undefined") {
    old_plot_data.destroy();
  }
  color_gradient = ["#FF0000"]
  for (var i = 17;i < 256; ) {
    color_gradient.push( "#10" + i.toString(16) + "EA" );
    i = i + 2;
  } 
  for (var i = 230;i > 17; ) {
    color_gradient.push( "#10FF" + i.toString(16) );
    i = i - 2;
  } 
	var plot = $.plot(graph_div, metrics,  {
		xaxis: {
			mode: "time",
			timeformat: "%Y/%m/%d %H:%M",
			timezone: "browser",
			min: _min,
			max: _max,
			zoomRange: [60*60*1000,60*60*24*7*1000] // X axis can't be closer than 1 hour or further than 7 days 
		},
		series: {
			points: { show: false },
			lines: { show: true }
		},
		pan: {
			interactive: true
		},
		grid: {
			hoverable: true,
			clickable: true
		},
    legend: {
      position: "nw"
    },
    colors: color_gradient
	});

	$(graph_div).bind("plothover", function(event, pos, item) {
		if (item) {
      point_time = new Date(item.datapoint[0]);
			item_label = "";
			if (item.series.label !== undefined) {
				item_label = item.series.label + ": ";
			}
      if (item.series.epoch !== undefined) {
        item_label = "-"+Math.round((point_time.getTime() - epochToTime(item.series.epoch)) / 3600000)+" Hour(s): ";
      }
			text = item_label + item.datapoint[1] + " " + unit + " - " + point_time.toString().slice(0,24);
			span = $('<span id="dummy-hover-span" style="display:none;">'+text+'</span>');
			$('body').append(span);
			width = $('#dummy-hover-span').width();
			if (item.pageX - (width/2) < 0) {
				width = 0;
			}
			showTooltip(item.pageX-(width/2), item.pageY, text);
			$('#dummy-hover-span').remove();
		} else {
			$('#tooltip').remove();
		}
	});
 
	return plot;
}

function showTooltip(x, y, contents) {
	if ($('#tooltip').text() !== contents) {
		$('#tooltip').remove();
	} else {
		return;
	}
	$('<div id="tooltip">' + contents + '</div>').css( {
		position: 'absolute',
		display: 'none',
		top: y + 20,
		left: x + 10,
		border: '1px solid #fdd',
		padding: '2px',
		'background-color': '#fee',
		opacity: 0.80
	}).appendTo("body").fadeIn(200);
}

function parseReadGraphData(data) {
  var temp_graph_data = [];
  var delta_graph_data = [];
  var observation_data = []

	min = Number.MAX_VALUE;
	max = Number.MIN_VALUE;

  $.each( data.observation_data, function( index, observation ) {
		var time = epochToTime(observation.observation_epoch);
    if (min > time) {
      min = time;
    }
    if (max < time) {
      max = time;
    }
		observation_data.push([time, parseFloat(observation.measured_temp)]);
	});
  temp_graph_data.push({data:observation_data, label:"Observed Temperatures", lines:{lineWidth: 7}});

  var collected_forecasts = data.collected_forecasts;
  $.each( data.collected_forecasts, function( index, collected_forecast ) {
    single_forecast = []
    single_forecast_delta = []
    $.each( collected_forecast.forecast, function( index, hour_forecast ) { 
      var forecast_time = epochToTime(hour_forecast.forecast_epoch)
      var forecast_temp = parseFloat(hour_forecast.forecast_temp);
      var closest_observation_temp = locateClosestObservationToForecastTime(observation_data, forecast_time);
      single_forecast.push([forecast_time, forecast_temp]);
      single_forecast_delta.push([forecast_time, forecast_temp - closest_observation_temp]);
    });
    temp_graph_data.push({data:single_forecast, epoch:collected_forecast.collection_epoch});
    delta_graph_data.push({data:single_forecast_delta, epoch:collected_forecast.collection_epoch});
  });
	drawGraph($('#temp_graph'), temp_graph_data, 'F', min, max);
  drawGraph($('#temp_delta_graph'), delta_graph_data, 'F', min, max);
};

function epochToTime(epoch) {
  return (new Date(parseFloat(epoch)*1000)).getTime();
}

function locateClosestObservationToForecastTime(observation_data, forecast_time) {
  var closest_time = Math.abs(forecast_time - observation_data[0][0]);
  var closest_observation = observation_data[0][1];
  $.each( observation_data, function( index, observation ) {
    var time_delta = Math.abs(forecast_time - observation[0]);
    if (time_delta < closest_time) {
      closest_time = time_delta;
      closest_observation = observation[1];
    } else if (time_delta == closest_time) {
      // Take the average
      closest_observation = (closest_observation + observation[1])/2;
    }
  });
 
  return closest_observation;
}

$.getJSON("/read/weather", parseReadGraphData);
