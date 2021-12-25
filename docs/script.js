// CHART DATA AND FUNCTIONS
function buildPlot1(plot_specs) {
  console.log(plot_specs);
  if (plot_specs == 'Spend Threshold') {
    var response = localStorage.getItem('monthly2');
    var data = JSON.parse(response);
  } else if (plot_specs == 'Time-Based') {
    var response = localStorage.getItem('monthly3');
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
  // var selected = document.getElementsByClassName('btn disabled')[0].innerHTML;
  var selected = plot_specs;
  if (selected == "Top/Bottom 10%") {
    compare = "Decile"
  } else if (selected == "Top/Bottom Quartile") {
    compare = "Quartile"
  } else if (selected == "Above/Below Median") {
    compare = "Median"
  } else if (selected == "Spend Threshold") {
    compare = "Threshold"
  } else if (selected == "Time-Based") {
    compare = "Time"
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
    options1['plotOptions']['bar']['borderRadius'] = 10
  } else if (compare == 'Time') {
    var category_raw = data["Date"];
    var key1 = Object.keys(data)[1];
    var key2 = Object.keys(data)[2];
    console.log(key2)
    var top = [];
    var bottom = [];
    var categories = [];
    
    var maxy = 0;
    var series = []
    var colors = []
    colors.push("#00E396")
    // colors.push("#008FFB")
    colors.push("#FF4560")
    console.log(data)

    
    for(var i in category_raw) {
      
      categories.push(data["Date"][i]);
      top.push(data[key1][i]);
      bottom.push(data[key2][i]);
    };

    var series = [{
      name: key2,
      data: bottom
    }, {
      name: key1,
      data: top,
    }
    ]
    options1['series'] = series;
    options1['plotOptions']['bar']['distributed'] = false
    options1['plotOptions']['bar']['borderRadius'] = 0
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
    options1['plotOptions']['bar']['borderRadius'] = 10
  }
  
  
  // update objects
  options1['colors'] = colors;
  // options1['yaxis']['max'] = maxy+maxy*.10;

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
  } else if (plot_specs == "Spend Threshold") {
    var response = localStorage.getItem('category5');
    var data = JSON.parse(response);
  } else if (plot_specs == "Time-Based") {
    var response = localStorage.getItem('category6');
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
  } else if (plot_specs == "Spend Threshold") {
    var category_raw = data["Category"];
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
      
      categories.push(data["Category"][i]);
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
    ]} else if (plot_specs == 'Time-Based') {
      var category_raw = data["Category"];
      var key1 = Object.keys(data)[1];
      var key2 = Object.keys(data)[2];
      console.log(key2)
      var top = [];
      var bottom = [];
      var categories = [];
      
      var maxy = 0;
      var series = []
      var colors = []
      
      // colors.push("#008FFB")
      colors.push("#FF4560")
      colors.push("#00E396")
      console.log(data)
  
      
      for(var i in category_raw) {
        
        categories.push(data["Category"][i]);
        top.push(data[key1][i]);
        bottom.push(data[key2][i]);
      };
  
      var series = [{
        name: key1,
        data: top,
      }, {
        name: key2,
        data: bottom
      }, 
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
  $('.btn-primary').click(function () {
    $('.btn-primary').removeClass('disabled');
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
  }
}
function handleMonthly2() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('monthly2', this.responseText)
  }
}
function handleMonthly3() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('monthly3', this.responseText)
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
function handleCategory5() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('category5', this.responseText)
  }
}
function handleCategory6() {
  if (successfulRequest(this)) {
    var response = JSON.parse(this.responseText);
    localStorage.setItem('category6', this.responseText)
  }
}

var base_url = "https://raw.githubusercontent.com/wesleybeckner/mintdash/main/examples/static_data/";

ajaxRequest("GET", base_url + "monthly_spending.json", handleMonthly);
ajaxRequest("GET", base_url + "monthly_spending_threshold.json", handleMonthly2);
ajaxRequest("GET", base_url + "monthly_spending_time.json", handleMonthly3);
ajaxRequest("GET", base_url + "category_spending_none.json", handleCategory1);
ajaxRequest("GET", base_url + "category_spending_10.json", handleCategory2);
ajaxRequest("GET", base_url + "category_spending_25.json", handleCategory3);
ajaxRequest("GET", base_url + "category_spending_50.json", handleCategory4);
ajaxRequest("GET", base_url + "category_spending_threshold.json", handleCategory5);
ajaxRequest("GET", base_url + "category_spending_time.json", handleCategory6);

options2 = buildPlot2('None');
var chart = new ApexCharts(document.querySelector("#chart2"), options2);
chart.render();

options1 = buildPlot1('None');
var chart = new ApexCharts(document.querySelector("#chart1"), options1);
chart.render();

// FILE UPLOAD
	
$(document).ready(function() {

	function FinanceProcessor() {	
		var newStats = new Stats();
		//Call Methods
		newStats.init();	
		newStats.collectTables();
		//Update View
		// updateDom();
	};

	//Create Stats class
	var Stats = function(cleanedData){
		this.cleanedData = cleanedData;
	};
	
	// init method - prepares data for processing, sets all Stats properties to default values
	Stats.prototype.init = function(){
    var dates = $(data).map(function(){ return this.Date; });
    var categories = $(data).map(function(){ return this.Category; });
    var amounts = $(data).map(function(){ return this.Amount; });
		
		//combine arrays
		cleanedData = {"Date": dates, 
                   "Category": categories,
                   "Amount": amounts};	
    console.log(cleanedData);
	};

	// Calculate and output the required statistics
	Stats.prototype.collectTables = function() {
    $('.datlearn').addClass('datlearn--show');
    
    var rdydata = JSON.stringify(data);
    
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = false;

    xhr.addEventListener("readystatechange", function() {
      if(this.readyState === 4) {
        raw = this.responseText;
        data = JSON.parse(raw);
      
        localStorage.setItem('monthly', data[0]);
        localStorage.setItem('monthly2', data[1]);
        localStorage.setItem('monthly3', data[2]);
        localStorage.setItem('category1', data[3]);
        localStorage.setItem('category2', data[4]);
        localStorage.setItem('category3', data[5]);
        localStorage.setItem('category4', data[6]);
        localStorage.setItem('category5', data[7]);
        localStorage.setItem('category6', data[8]);
        console.log("successful import");
        
        $('.datlearn').removeClass('datlearn--show');

        $('.btn-primary').removeClass('disabled');
        $('none-button').addClass('disabled');
        var selected = "None"

        // MONTHLY
        options1 = buildPlot1(selected);
        ApexCharts.exec('timeseries', 'updateOptions', options1);

        // CATEGORY
        options2 = buildPlot2(selected);
        ApexCharts.exec('categories', 'updateOptions', options2);

      }
    });

    xhr.open("POST", "https://mintdash.azurewebsites.net/freeze/");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send(rdydata);
	};

	//File Upload

	// Confirm browser supports HTML5 File API
	var browserSupportFileUpload = function() {
		var isCompatible = false;
		if(window.File && window.FileReader && window.FileList && window.Blob) {
			isCompatible = true;
		}
		return isCompatible;
	};

	// Upload selected file and create array
	var uploadFile = function(evt) {
		var file = evt.target.files[0];
		var reader = new FileReader();
		reader.readAsText(file);
		reader.onload = function(event) {
			//Jquery.csv
			createArray($.csv.toObjects(event.target.result));			
		};
	};

	// Validate file import
	var createArray = function(data) {	
		if(data !== null && data !== "" && data.length > 1) {
			this.data = data;
      console.log(data);
			FinanceProcessor(data);
		} else {
		}	
	};
	
	// event listener for file upload
	if (browserSupportFileUpload()) {
			document.getElementById('txtFileUpload').addEventListener('change', uploadFile, false);
		} else {
			$("#introHeader").html('The File APIs is not fully supported in this browser. Please use another browser.');
		}	
});

$(document).ready(function () {
  var xhr = new XMLHttpRequest();
  xhr.withCredentials = false;

  xhr.addEventListener("readystatechange", function() {
    if(this.readyState === 4) {
      console.log(this.responseText);
    } else if (this.status == 400) {
      $("#txtFileUpload").attr('disabled', 'disabled');
      document.getElementById('serverStatus').style = "display:block;";
    }
  });

  xhr.open("GET", "https://mintdash.azurewebsites.net/freeze/");

  xhr.send();
})