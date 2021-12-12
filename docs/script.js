// CHART DATA AND FUNCTIONS
function buildPlot1(plot_specs) {
  console.log(plot_specs);
  if (plot_specs == 'Spend Threshold') {
    var response = localStorage.getItem('monthly2');
    var data = JSON.parse(response);
  } else {
    var response = localStorage.getItem('monthly');
    var data = JSON.parse(response);
  } 
  var amount = data["Amount"];
  var result = [];
  var colors = [];
  var maxy = 0;

  // Decile Quartile or Median
  var compare = "Quartile"
  var selected = document.getElementsByClassName('btn disabled')[0].innerHTML;
  if (selected == "Top/Bottom 10%") {
    compare = "Decile"
  } else if (selected == "Top/Bottom Quartile") {
    compare = "Quartile"
  } else if (selected == "Above/Below Median") {
    compare = "Median"
  } else if (selected == "Spend Threshold") {
    compare = "Threshold"
  } else {
    compare = "None"
  }
  
  if (compare == "Threshold") {
    var category_raw = data["Date"];
    var top = [];
    var middle = [];
    var bottom = [];
    var categories = [];
    
    var maxy = 0;
    var series = []
    var colors = []
    colors.push("#00E396")
    
    colors.push("#008FFB")
    colors.push("#FF4560")
    console.log(data)

    
    for(var i in category_raw) {
      
      categories.push(data["Date"][i]);
      top.push(data["greater than 150"][i]);
      bottom.push(data["less than 20"][i]);
      middle.push(data["between 20 and 150"][i]);
    };

    var series = [{
      name: 'Less than 20',
      data: bottom
    }, {
      name: 'Between 20 and 150',
      data: middle,
    }, {
      name: 'Greater than 150',
      data: top,
    }
    ]
    options1['series'] = series;
    options1['plotOptions']['bar']['distributed'] = false
    // plotOptions: {
    //   bar: {
    //     distributed: true,
    //     borderRadius: 10,
    //     dataLabels: {
    //       position: 'top', // top, center, bottom
    //     },
    //   }
    // },
  } else {
    for(var i in amount) {
      result.push(amount[i]);
  
      if (parseInt(amount[i]) > maxy) {
        maxy = parseInt(amount[i])
        
      };
  
      if (compare != "None") {
        if (data[compare][i] == 'Top') {
          colors.push("#FF4560")
        }
        else if (data[compare][i] == 'Bottom') {
          colors.push("#00E396")
        }
        else {
          colors.push("#008FFB")
        }
      } else {
        colors.push("#008FFB")
      }
      
    };
    var series = [{
      name: 'hehe',
      data: result,
    }]
    options1['series'] = series;
    options1['plotOptions']['bar']['distributed'] = true
  }
  
  
  // update objects
  
  
  options1['colors'] = colors;
  options1['yaxis']['max'] = maxy+maxy*.10;

  return options1
}

function buildPlot2(plot_specs) {
  // for 10,25,50 datasets (from request)
  // name: the Quantile
  // data: the Amount
  // category: the Category
  if (plot_specs == 'None') {
    var response = localStorage.getItem('category1');
    var data = JSON.parse(response);
  } else if (plot_specs == "Top/Bottom 10%") {
    var response = localStorage.getItem('category2');
    var data = JSON.parse(response);
  } else if (plot_specs == "Top/Bottom Quartile") {
    var response = localStorage.getItem('category3');
    var data = JSON.parse(response);
  } else if (plot_specs == "Above/Below Median") {
    var response = localStorage.getItem('category4');
    var data = JSON.parse(response);
  }

  if (plot_specs == 'None') {
    var category_raw = data["Category"];
    var amount = [];
    var colors = [];
    var categories = [];
    colors.push("#008FFB")
    for(var i in category_raw) {
        categories.push(data["Category"][i]);
        amount.push(data["Amount"][i]);
    };

    var series = [{
      name: 'Middle',
      data: amount,
    }
    ]
  } else if (plot_specs == "Above/Below Median"){
    var category_raw = data["Category"];
    var top = [];
    var bottom = [];
    var categories = [];
    
    var maxy = 0;
    var series = []
    var colors = []
    colors.push("#FF4560")
    colors.push("#00E396")

    
    for(var i in category_raw) {
      
      categories.push(data["Category"][i]);
      top.push(data["Top"][i]);
      bottom.push(data["Bottom"][i]);
    };

    var series = [{
      name: 'Top',
      data: top,
    }, {
      name: 'Bottom',
      data: bottom
    }
    ]
  } else {
    var category_raw = data["Category"];
    var top = [];
    var middle = [];
    var bottom = [];
    var categories = [];
    
    var maxy = 0;
    var series = []
    var colors = []
    colors.push("#FF4560")
    colors.push("#008FFB")
    colors.push("#00E396")

    
    for(var i in category_raw) {
      
      categories.push(data["Category"][i]);
      top.push(data["Top"][i]);
      bottom.push(data["Bottom"][i]);
      middle.push(data["Middle"][i]);
    };

    var series = [{
      name: 'Top',
      data: top,
    }, {
      name: 'Middle',
      data: middle,
    }, {
      name: 'Bottom',
      data: bottom
    }
    ]
  }

  // update objects

  options2['xaxis']['categories'] = categories;
  options2['colors'] = colors;
  options2['series'] = series;

  return options2
}

var options1 = {
legend: {
  show: false,
},
  series: [{
  name: 'Total Spending',
  data: [10,10,10],
}],
  chart: {
  stacked: true,
  height: 350,
  type: 'bar',
  id: 'timeseries',
  animations: {
    dynamicAnimation: {
        enabled: true,
        speed: 350
    }
},
},
plotOptions: {
  bar: {
    distributed: true,
    borderRadius: 10,
    dataLabels: {
      position: 'top', // top, center, bottom
    },
  }
},
dataLabels: {
  enabled: true,
  formatter: function (val) {
    return val;
  },
  offsetY: -20,
  style: {
    fontSize: '12px',
    colors: ["#304758"]
  }
},

xaxis: {
  categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  position: 'top',
  axisBorder: {
    show: false
  },
  axisTicks: {
    show: false
  },
  crosshairs: {
    fill: {
      type: 'gradient',
      gradient: {
        colorFrom: '#D8E3F0',
        colorTo: '#BED1E6',
        stops: [0, 100],
        opacityFrom: 0.4,
        opacityTo: 0.5,
      }
    }
  },
  tooltip: {
    enabled: true,
  }
},
yaxis: {
  axisBorder: {
    show: false
  },
  axisTicks: {
    show: false,
  },
  labels: {
    
    show: false,
    formatter: function (val) {
      return val;
    }
  }

},
title: {
  text: 'Monthly Spending, 2021',
  floating: true,
  offsetY: 330,
  align: 'center',
  style: {
    color: '#444'
  }
}
};

var options2 = {
  legend: {
    show: false,
  },
    series: [{
    name: 'Total Spending',
    data: [10,10,10],
  }],
    chart: {
    height: 350,
    type: 'bar',
    id: 'categories',
    stacked: true,
    animations: {
      dynamicAnimation: {
          enabled: true,
          speed: 350
      }
  },
  },
  plotOptions: {
    bar: {
      // distributed: true,
      borderRadius: 0, // for rounded bars
      dataLabels: {
        position: 'top', // top, center, bottom
      },
    }
  },
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      return val;
    },
    offsetY: -20,
    style: {
      fontSize: '12px',
      colors: ["#304758"]
    }
  },
  
  xaxis: {
    categories: ["Jan", "Feb", "Mar"],
    position: 'bottom',
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    },
    crosshairs: {
      fill: {
        type: 'gradient',
        gradient: {
          colorFrom: '#D8E3F0',
          colorTo: '#BED1E6',
          stops: [0, 100],
          opacityFrom: 0.4,
          opacityTo: 0.5,
        }
      }
    },
    tooltip: {
      enabled: true,
    }
  },
  yaxis: {
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false,
    },
    labels: {
      
      show: false,
      formatter: function (val) {
        return val;
      }
    }
  
  },
  title: {
    text: 'Category Spending, Monthly Averages',
    floating: true,
    offsetY: 330,
    align: 'center',
    style: {
      color: '#444'
    }
  }
  };

// DROPDOWN LOGIC
$(document).ready(function () {
  $('.btn').click(function () {
    $('.btn').removeClass('disabled');
    $(this).addClass('disabled');
    var selected = document.getElementsByClassName('btn disabled')[0].innerHTML;

    // MONTHLY
    options1 = buildPlot1(selected);
    ApexCharts.exec('timeseries', 'updateOptions', options1);

    // CATEGORY
    options2 = buildPlot2(selected);
    ApexCharts.exec('categories', 'updateOptions', options2);
  })
})

// AJAX AND DATA HANDLING
function ajaxRequest(method, url, handlerFunction) {
  const xhttp = new XMLHttpRequest();
  xhttp.withCredentials = false;
  xhttp.open(method, url);
  xhttp.onreadystatechange = handlerFunction;
  xhttp.send();
}

function successfulRequest(request) {
  return request.readyState === 4 && request.status == 200;
}

function errorMsg() {
  console.log("Ready state: " + this.readyState);
  console.log("Status: " + this.status);
  console.log("Status text: " + this.statusText);
}

// MONTHLY 
function handleMonthly() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('monthly', this.responseText)
    options1 = buildPlot1(response);
    var chart = new ApexCharts(document.querySelector("#chart1"), options1);
    chart.render();
    
  }
}
function handleMonthly2() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('monthly2', this.responseText)
  }
}

// CATEGORY
function handleCategory1() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('category1', this.responseText)
  }
}
function handleCategory2() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('category2', this.responseText)
  }
}
function handleCategory3() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('category3', this.responseText)
  }
}
function handleCategory4() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('category4', this.responseText)
  }
}

var base_url = "https://raw.githubusercontent.com/wesleybeckner/mintdash/main/examples/static_data/";

ajaxRequest("GET", base_url + "monthly_spending.json", handleMonthly);
ajaxRequest("GET", base_url + "monthly_spending_threshold.json", handleMonthly2);
ajaxRequest("GET", base_url + "category_spending_none.json", handleCategory1);
ajaxRequest("GET", base_url + "category_spending_10.json", handleCategory2);
ajaxRequest("GET", base_url + "category_spending_25.json", handleCategory3);
ajaxRequest("GET", base_url + "category_spending_50.json", handleCategory4);

options2 = buildPlot2('None');
var chart = new ApexCharts(document.querySelector("#chart2"), options2);
chart.render();