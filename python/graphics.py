#!/usr/bin/python
import json
import gviz_api
import datetime

page_template = open("templates/template_1.html", "r").read()

def main():
    #Creating schema
    description = {"user": ("string", "User name"),
                 "commits": ("number", "Number of user commits")}
    description2 = {"day": ("string", "Day"),
                 "commits": ("number", "Number of user commits")}
    description3 = {"date": ("date", "Date"),
                 "commits": ("number", "Number of user commits")}
    description4 = {"proy": ("string", "Project name"),
                 "commits": ("number", "Numero de commits")}
    description5 = {"date": ("date", "Date"),
                 "commits": ("number", "Number of user commits")}

    #Loading files
    with open('data/test.json') as json_file:
        data = json.load(json_file)

    with open('data/test2.json') as json_file2:
        data2 = json.load(json_file2)

    with open('data/test5.json') as json_file3:
        data3 = json.load(json_file3)

    with open('data/test6.json') as json_file4:
        data4 = json.load(json_file4)

    with open('data/test7.json') as json_file5:
        data5 = json.load(json_file5)    

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    data_table2 = gviz_api.DataTable(description2)
    data_table2.LoadData(data2)

    for i in range(len(data3)):
        data3[i]['date'] = datetime.datetime.strptime(data3[i]['date'],'%Y-%m-%d')

    data_table3 = gviz_api.DataTable(description3)
    data_table3.LoadData(data3)

    data_table4 = gviz_api.DataTable(description4)
    data_table4.LoadData(data4)

    for i in range(len(data5)):
        data5[i]['date'] = datetime.datetime.strptime(data5[i]['date'],'%Y-%m-%d')

    data_table5 = gviz_api.DataTable(description5)
    data_table5.LoadData(data5)

    # Creating a JavaScript code string
    jscode = data_table.ToJSCode("jscode_data",
                                columns_order=("user", "commits"))

    jscode2 = data_table2.ToJSCode("jscode2_data",
                                columns_order=("day", "commits"))

    jscode3 = data_table3.ToJSCode("jscode3_data",
                                columns_order=("date", "commits"))

    jscode4 = data_table4.ToJSCode("jscode4_data",
                                columns_order=("proy", "commits"))

    jscode5 = data_table5.ToJSCode("jscode5_data",
                                columns_order=("date", "commits"))

    #json1 = data_table3.ToJSon(columns_order=("proy", "day", "commits"))
    #print json1

    # Putting the JS code into the template
    pagina = page_template % vars()

    f= open("test/prueba.html","w+")
    f.write(pagina)
    f.close() 

if __name__ == "__main__":
    main()