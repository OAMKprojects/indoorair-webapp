function reload_database()
{
    $.ajax({
    type : "GET",
    url : '/reload_db',
    dataType: "json",
    contentType: 'application/json;charset=UTF-8',
    success: function (data) {
            $('#temp_val').html(data["temperature"] + " °C");
            $('#hum_val').html(data["humidity"] + " %");
            $('#text').text(data["text"]);
            $('#background').removeClass().addClass(data["image"]);
        }
    });
    setTimeout(reload_database, 2000);
}

function load_chart_data(data_type, sufix, min_y, max_y, hours)
{
    $.ajax({
    type : "POST",
    url : "/load_db_val",
    dataType: "json",
    contentType: "application/json; charset=UTF-8",
    data : JSON.stringify({"datatype" : data_type}),
    success: function (data) {
        
            var values = data[data_type];
            var data_points = [];
            for (var i = 0; i < values.length; i++) {
                data_points.push({
                    x : new Date(values[i].x),
                    y : values[i].y
                });
            }
            var max_time = new Date(new Date().getTime());
            var min_time = new Date(new Date().getTime());
            min_time.setHours(min_time.getHours() - hours);
            var chart = new CanvasJS.Chart("chart", {
                height: 400,
                title : {
                    text : data_type,
                    fontColor: "grey"
                },
                data : [{
                    type : "spline",
                    markerSize: 0,
                    dataPoints : data_points
                }],
                axisY: {
                    suffix: sufix,
                    minimim: min_y,
                    maximum: max_y
                },
                axisX: {
                    valueFormatString: "MMM DD HH:mm",
                    maximum: max_time,
                    minimum: min_time
                },
            });
            chart.render();
        }
    });
}