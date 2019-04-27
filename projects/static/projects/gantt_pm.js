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
     if (i < 1) {
       gantt_data.push([String(i), k[i][0], k[0][0], new Date(k[i][1]), new Date(k[i][2]), null, null, null]);

     }
     else {
       gantt_data.push([String(i), k[i][0], 'PM', new Date(k[i][1]), new Date(k[i][2]), null, null, String(i-1)]);
     }
   }

   otherData.addRows(gantt_data);

   var options = {
     height: 400;
     gantt: {
      trackHeight: 20,
      barHeight: 15,
      labelStyle: {
      fontName: 'Courier',
      },
      criticalPathEnabled: false, // Critical path arrows will be the same as other arrows.
      arrow: {
        width: 1,
        color: 'red',
        radius: 0
      },
    }
  };


   var chart = new google.visualization.Gantt(document.getElementById('chart_div'));

   chart.draw(otherData, options);
 }
}
