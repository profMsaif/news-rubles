// ГРАФИК ДОЛЛАР_РУБЛЬ (ПРИ ЗАГРУЗКИ СТРАНИЦЫ)
var chart = Highcharts.chart('container-chartt', {
    chart: {
        type: 'line'
    },
    title: {
        text: ''
    },
    subtitle: {
        text: 'Доллар/Рубль'
    },
    xAxis: {
        categories: data_usd.charts_currency.dates_list
    },
    yAxis: {
        title: {
            text: 'Exchange rate'
        }
    },
    plotOptions: {
        line: {
            marker: {
                enabled: false,
                symbol: 'circle',
                radius: 2,
                states: {
                    hover: {
                        enabled: true
                    }
                }
            }
        }
    },
    series: data_usd.charts_currency.series
});
