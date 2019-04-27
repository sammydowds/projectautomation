function ganttCreator(k) {

 google.charts.load('current', {'packages':['gantt']});
 google.charts.setOnLoadCallback(drawChart);

 function drawChart() {

   var otherData = new google.visualization.DataTable();
   otherData.addColumn('string', 'Task ID');
   otherData.addColumn('string', 'Task Name');
   otherData.addColumn('string', 'Resource');
   otherData.addColumn('date', 'Start Date');
   otherData.addColumn('date', 'End Date');
   otherData.addColumn('number', 'Duration');
   otherData.addColumn('number', 'Percent Complete');
   otherData.addColumn('string', 'Dependencies');

   var gantt_data = [];
   for (var i = 0; i < k.length; i++) {
     console.log(k[i][1]);
     console.log(k[i][2]);
     console.log('done');
     if (i == 0) {
       gantt_data.push([String(i), k[i][0], k[0][0], new Date(k[i][1]), new Date(k[i][2]), null, null, null]);
     }
     else if (i == 1) {
       gantt_data.push([String(i), k[i][0], k[1][0], new Date(k[i][1]), new Date(k[i][2]), null, null, null]);
     }
     else if (i > 1) {
       gantt_data.push([String(i), k[i][0], k[1][0], new Date(k[i][1]), new Date(k[i][2]), null, null, String(i-1)]);
     }
   }

   otherData.addRows(gantt_data);

   var options = {
     height: 350,
     gantt: {
      trackHeight: 40,
      barHeight: 25,
      barCornerRadius: 1,
      labelMaxWidth: 400,
      labelStyle: {
      fontName: 'Courier',
      },
      criticalPathEnabled: false, // Critical path arrows will be the same as other arrows.
      arrow: {
        angle: 100,
        width: 1,
        lenght: 10,
        color: 'red',
        radius: 0,
        spaceAfter: 6
      },
      innerGridTrack: {
        fill: 'white'
      },
      innerGridDarkTrack: {
        fill: 'white'
      },
      innerGridHorizLine: {
            stroke: 'white',
            strokeWidth: 2
          },
    }
  };


   var chart = new google.visualization.Gantt(document.getElementById('chart_div'));

   chart.draw(otherData, options);
 }
}
