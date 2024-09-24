window.onload = function() {
    var num_periods = js_vars.num_periods
    var labels = js_vars.labels
    let price_data = js_vars.price_data
    let volume_data = js_vars.volume_data
    let suggest_max = Math.max(...price_data) * 1.2;

    function pad_val(value, index, values) {
        let tick = ('' + value).padStart(4, ' ');
        tick.replace(' ', 'nbsp;');
        return tick;
    }

    function pad_val2(value, index, values) {
        let tick = ('' + value).padStart(5, ' ');
        tick.replace(' ', 'nbsp;');
        return tick;
    }

    var ctx_price = document.getElementById('gr_price');
    var price_chart = new Chart(ctx_price, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Call Price',
                data: price_data,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1

            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {display: false},
            scales: {
                xAxes: [{display: false}],
                yAxes: [{
                    scaleLabel: {
                        display: true
                        , labelString: "Price"
                        , fontSize: 18
                    },
                    ticks: {
                        callback: pad_val
                        , suggestedMax: suggest_max
                        , suggestedMin: 0.00
                    }
                }],
            },
            animation: {duration: 0},
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 0,
                    bottom: 0
                }
            }
        }
    });

    var ctx_vol = document.getElementById('gr_volume');
    var vol_chart = new Chart(ctx_vol, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Volume',
                data: volume_data,
                fill: true,
                borderColor: 'rgb(192, 192, 192)',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 5,
            legend: {display: false},
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true
                        , labelString: "Volume"
                        , fontSize: 18
                    },
                    ticks: {
                        callback: pad_val2
                        , beginAtZero: true
                        , suggestedMax: 4
                        , stepSize: 1

                    }

                }],
            },
            animation: {duration: 0}
        }
    });

    let market_history = {
        num_periods: num_periods,
        labels: labels,
        prices: price_data,
        volumes: volume_data
    };

    console.log(JSON.stringify(market_history, null, 2));
    console.log('Price history loaded');
}