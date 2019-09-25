#!/usr/bin/python
import json
import os
import gviz_api
import datetime

page_template = open("templates/template_1.html", "r").read()

def loadFile(file):
    with open(file) as json_file:
      return json.load(json_file)

def parseDate(data):
    for i in range(len(data)):
        data[i]['date'] = datetime.datetime.strptime(data[i]['date'],'%Y-%m-%d')
    return data

def createAndLoadDataTable(description, data):
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    return data_table

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
    description6 = {"day": ("string", "Day"),
                  "proy1": ("number", "Commits proyecto 1"),
                  "proy2": ("number", "Commits proyecto 2"),
                  "proy3": ("number", "Commits proyecto 3")}

    description_aut = {"Autor": ("string", "Nombre del autor"),
                  "Porcentaje": ("number", "Porcentaje de commits en el repositorio")}

    #Loading files and assigning variables
    data = loadFile('data/test.json')
    data2 = loadFile('data/test2.json')
    data3 = loadFile('data/test5.json')
    data4 = loadFile('data/test6.json')
    data5 = loadFile('data/test7.json')  
    data6 = loadFile('data/test3.json')

    data_aut = loadFile('data/data-minishift.json')
    proy_aut = data_aut['Nombre repositorio']
    comm_aut = data_aut['Commits totales']
    user_aut = data_aut['Contribuidores totales']

    #Preparing data
    data3 = parseDate(data3)
    data5 = parseDate(data5)

    # Loading it into gviz_api.DataTable
    data_table = createAndLoadDataTable(description,data)
    data_table2 = createAndLoadDataTable(description2,data2)
    data_table3 = createAndLoadDataTable(description3,data3)
    data_table4 = createAndLoadDataTable(description4,data4)
    data_table5 = createAndLoadDataTable(description5,data5)
    data_table6 = createAndLoadDataTable(description6,data6)
    data_table_aut = createAndLoadDataTable(description_aut,data_aut['Commits'])

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

    jscode6 = data_table6.ToJSCode("jscode6_data",
                                columns_order=("day","proy1", "proy2", "proy3"), 
                                order_by = "day")

    jscode_aut = data_table_aut.ToJSCode("jscode_aut_data",
                                columns_order=("Autor","Porcentaje"), 
                                order_by = "Porcentaje")

    # Putting the JS code into the template
    pagina = page_template % vars()


    if not os.path.isdir("generated"):
        os.mkdir("generated") 
    f= open("generated/prueba.html","w+")
    f.write(pagina)
    f.close() 

if __name__ == "__main__":
    main()