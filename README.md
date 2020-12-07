# Covid-19 Dash

The application shows Covid-19 information across the world, mainly different types of interactive visualization.

The first element of the web is a table that shows every country's data such as **total case**, **total death**, and **population**. 

![](/images/table.png)

Here are several features for the table:
* Hide columns 
* Sort values in each column (ascending or descending)
* Filter data in each column
* Delete or select multiple rows
* 6 rows per page and 32 pages in total (can switch pages)
* Interact with world map below

![](/images/map_selected.png)

First, the world choropleth map describes the Covid-19 information across the world. The color represents **logarithmic total case**. Blue/purple means small number of cases, while yellow/orange means large number of cases. In addition, by hovering countries on the map, users can see total case, total death, and population of each country. 

### Interacting with the table above
After selecting rows in the table, the border of selected country will be highlighted in light blue (US and China). However, after filtering countries, the map will only keep the filtered countries and the other countries will appear black. The filtering function is dispalyed below (only keeps European countries).

![](/images/map_filtered.png)


### Add customized graphs

Two types of graphs are available:
* Bar chart
* Line chart

#### Bar Chart
In bar chart, X axis is countries. Y axis can be one of the following: *Total Case*, *Total Death*, *Population*, *GDP/Capita*, *Life Expectancy*. 

![](/images/bar_chart.png)

#### Line Chart
In line chart, X axis is countries. Y axis can be one of the following: *Total Case*,*New Case*,*Total Death*,*New Death*.  

![](/images/line_chart.png)

Users can keep adding charts and compare among them. 

![](/images/multiple_charts.png)












