function chartStyle(k) {
  console.log(k);
  for (let key in k) {
    var dataDates = [];
    var projects = k[key];
    for (var i = 0; i < projects.length; i++) {
      var today = new Date();
      today.setMonth(today.getMonth() + i);
      today.setDate(1);
      dataDates.push({x: today, y: projects[i]});
    }
    var chart = new CanvasJS.Chart(key,
    {
      title:{
        text: "Capacity - Next 12 Months",
        fontFamily: "Courier"

    },
    axisX:{
        title: "Dates",
        interval: 1,
        intervalType: "months",
        gridThickness: 1,
        valueFormatString: "MMM-YY" ,
        labelAngle: -50,
        intervalType: "month"
    },
    axisY: {
        title: "Number of Jobs"
    },
    data: [
    {
        type: "area",
        color: "rgba(189, 0 , 0, 0.8)",
        dataPoints: dataDates
    }
    ]
  });

    chart.render();
  }

  }
