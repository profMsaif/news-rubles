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

// ГРАФИК ДОЛЛАР_РУБЛЬ (ПРИ НАЖАТИИ)

function graph_us_rub() {
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
}

// ГРАФИК ЕВРО_РУБЛЬ (ПРИ НАЖАТИИ)

function graph_eur_rub() {
    var chart = Highcharts.chart('container-chartt', {
        chart: {
            type: 'line'
        },
        title: {
            text: ''
        },
        subtitle: {
            text: 'Евро/Рубль'
        },
        xAxis: {
            categories: data_eur.charts_currency_eur.dates_list_eur
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
        series: data_eur.charts_currency_eur.series_eur
    });
}
// ГРАФИК С ПРЕДСКАЗАНИЕМ (ПРИ НАЖАТИИ)

function graph_forecast() {
    var chart = Highcharts.chart('container-chartt', {
        chart: {
            type: 'line'
        },
        title: {
            text: ''
        },
        subtitle: {
            text: 'Прогноз курса USD/EUR'
        },
        xAxis: {
            categories: data_forecast.charts_currency_forecast.date_l_seven
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
        series: data_forecast.charts_currency_forecast.series_forecast
    });
}