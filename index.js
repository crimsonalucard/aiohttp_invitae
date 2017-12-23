console.log("test");
axios.get('http://0.0.0.0:1337/?name=Brian')
    .then(function (response) {
        console.log(response);
        var div = document.createElement('div');
        var responseText = JSON.stringify(response.data);
        $(div).text(responseText).addClass('content');
        $(".main").append(div);
    })
    .catch(function (error) {
        console.log(error);
    });

axios.get('https://jsonplaceholder.typicode.com/comments')
    .then(function (response) {
        console.log(response);
        var chartData = response.data.map(function (row) {
            if (row["name"] !== null) {
                return row["name"].length;
            } else {
                return 0;
            }
        });
        console.log(chartData);
        var ctx = document.getElementById("myChart");
        var myLineChart = new Chart(ctx, {
            type: 'line',
            "data": {
                "labels": chartData.slice(0, 20).map(function (d, i) {
                    return i;
                }),
                "datasets": [{
                    "label": "My First Dataset",
                    "data": chartData.slice(0, 20),
                    "fill": false,
                    "borderColor": "rgb(75, 192, 192)",
                    "lineTension": 0
                }]
            },
            options: {}
        });

        new Chart(document.getElementById("myChart2"), {
            "type": "bar",
            "data": {
                "labels": response.data.map(function(row){return row.email;}).slice(0,6),
                "datasets": [{
                    "label": "My First Dataset",
                    "data": chartData.slice(0,6),
                    "fill": false,
                    "backgroundColor": ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)", "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)"],
                    "borderColor": ["rgb(255, 99, 132)", "rgb(255, 159, 64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)", "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)"],
                    "borderWidth": 1
                }]
            },
            "options": {"scales": {"yAxes": [{"ticks": {"beginAtZero": true}}]}}
        });

    }).catch(function (error) {
    console.log(error);
});
