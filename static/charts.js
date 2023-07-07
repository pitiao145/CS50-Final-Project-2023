document.addEventListener('DOMContentLoaded', function(){

// Make a chart to display the coffee bean stock.
// When the stock is too low, color in red
// When current batch is about to expire, gray

const ctx1 = document.getElementById('myChart1');
const ctx2 = document.getElementById('myChart2');
const ctx3 = document.getElementById('myChart3');
  // Get th elements with the bean names and stock amount from the table
  
  let table_labels = document.getElementsByClassName('bean_name');
  let table_stock = document.getElementsByClassName('bean_stock');
  var chart_type_query = {{ chart_data_type|tojson() }};
  var chart_origin_query = {{ chart_data_origin|tojson() }};
  
  var chart_labels = [];
  var chart_stock = [];
  var chart_type_labels = [];
  var chart_type_values = [];
  var chart_origin_labels = [];
  var chart_origin_values = [];
  
  //Populate a list for the labels and a list for the data.
  for (let i = 0; i < table_labels.length; i++) {
      chart_labels[i] = table_labels[i].innerHTML;
    }
  
  for (let i = 0; i < table_stock.length; i++) {
      chart_stock[i] = parseInt(table_stock[i].innerHTML); //Convert the string into floats
  }
  // Populate a list for the labels and values for both the origins and types chart
  for (let i = 0; i < chart_type_query.length; i++) {
      chart_type_labels[i] = chart_type_query[i]['type'];
      chart_type_values[i] = parseInt(chart_type_query[i]['n']);
  }
  for (let i = 0; i < chart_origin_query.length; i++) {
      chart_origin_labels[i] = chart_origin_query[i]['origin'];
      chart_origin_values[i] = parseInt(chart_origin_query[i]['n']);
  }
    // Checks      
  console.log('labels: ' + chart_labels);
  console.log('stocks: ' + chart_stock);
  console.log('type labels: ' + chart_type_labels);
  console.log('type values: ' + chart_type_values);
  console.log('origin labels: ' + chart_origin_labels);
  console.log('origin values: ' + chart_origin_values);
  
  new Chart(ctx1, {
      type: 'bar',
      data: {
        labels: chart_labels,
        datasets: [{
          label: 'Name',
          data: chart_stock,
          borderWidth: 1
        }]
  
      },
      options: {
          borderWidth: 5,
          borderRadius: 2,
          responsive: true
      }
    });

  new Chart(ctx2, {
        type: 'pie',
        data: {
          labels: chart_type_labels,
          datasets: [{
            label: 'Types',
            data: chart_type_values,
            borderWidth: 1
          }]
    
        },
        options: {
            borderWidth: 5,
            borderRadius: 2,
            responsive: true
        }
      });
    
  new Chart(ctx3, {
        type: 'pie',
        data: {
          labels: chart_origin_labels,
          datasets: [{
            label: 'Origins',
            data: chart_origin_values,
            borderWidth: 1
          }]
    
        },
        options: {
            borderWidth: 5,
            borderRadius: 2,
            responsive: true
        }
      });
    
    
});
    

