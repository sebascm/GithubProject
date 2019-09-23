#!/usr/bin/python
import json
import gviz_api

page_template = """
<html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      // Load the Visualization API and the required packages.
      google.charts.load('current', {'packages':['corechart']});
      google.charts.load('current', {'packages':['treemap']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.charts.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {
        %(jscode)s
        %(jscode2)s

        // var jsonString = (json3)s;
        // var array = JSON.parse(jsonString);
        // var dataTableData = google.visualization.arrayToDataTable(array);

        // Set chart options
        var options_pie = {'title':'Numero de commits',
                       'width':400,
                       'height':300};

        var options_lines = {
            title: 'Commits a lo largo del tiempo',
            curveType: 'function',
            lineWidth: 4,
            intervals: { 'style':'line' },
            legend: 'none'
        };

        var options_stacked = {
            isStacked: true,
            height: 300,
            legend: {position: 'top', maxLines: 3},
            hAxis: {minValue: 0}
        };

        // Instantiate and draw our chart, passing in some options.
        var chart_pie = new google.visualization.PieChart(document.getElementById('chart_pie_div'));
        chart_pie.draw(jscode_data, options_pie);

        var chart_lines = new google.visualization.LineChart(document.getElementById('chart_line_div'));
        chart_lines.draw(jscode2_data, options_lines);

        // var chart_bars = new google.visualization.BarChart(document.getElementById('chart_bar_div'));
        // chart_bars.draw(dataTableData, options_stacked);
      }
    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <div id="chart_pie_div"></div>
	<!--Div that will hold the line chart-->
    <div id="chart_line_div"></div>
    <!--Div that will hold the bar chart-->
    <div id="chart_bar_div"></div>
  </body>
</html>
"""

def main():
    #Creating schema
    description = {"user": ("string", "User name"),
                 "commits": ("number", "Number of user commits")}
    description2 = {"day": ("string", "Day"),
                 "commits": ("number", "Number of user commits")}
    description3 = {"proy": ("string", "Project ID"),
                 "day": ("string", "Day"),
                 "commits": ("number", "Number of user commits")}

    #Loading files
    with open('data/test.json') as json_file:
        data = json.load(json_file)

    with open('data/test2.json') as json_file2:
        data2 = json.load(json_file2)

    #with open('data/test3.json') as json_file3:
    #    data3 = json.load(json_file3)

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    data_table2 = gviz_api.DataTable(description2)
    data_table2.LoadData(data2)

    #data_table3 = gviz_api.DataTable(description3)
    #data_table3.LoadData(data3)

    # Creating a JavaScript code string
    jscode = data_table.ToJSCode("jscode_data",
                                columns_order=("user", "commits"))

    jscode2 = data_table2.ToJSCode("jscode2_data",
                                columns_order=("day", "commits"))

    #json3 = data_table3.ToJSon(columns_order=("proy", "day", "commits"),
    #                         order_by="proy")

    # Putting the JS code into the template
    pagina = page_template % vars()

    f= open("prueba.html","w+")
    f.write(pagina)
    f.close() 

if __name__ == "__main__":
    main()