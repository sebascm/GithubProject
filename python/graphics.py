#!/usr/bin/python
import json
import os
import gviz_api
import datetime
import ast

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

def loadScheme(file):
    with open(file, 'r') as f:
        s = f.read()
        return ast.literal_eval(s)

def main():
    #Creating schema
    description = loadScheme('data/test/schema')
    description2 = loadScheme('data/test2/schema')
    description3 = loadScheme('data/test5/schema')
    description4 = loadScheme('data/test6/schema')
    description5 = loadScheme('data/test7/schema')
    description6 = loadScheme('data/test3/schema')
    description7 = loadScheme('data/test12/schema')
    # description8 = { "inst": ("string", "Instancia (proyecto o usuario)"),
    #              "Parent": ("string", "Instancia padre (puede ser proyecto o usuario)"),
    #              "commits": ("number", "Numero de commits")}

    description_aut = loadScheme('data/test_aut/schema')

    #Loading files and assigning variables
    data = loadFile('data/test/data.json')
    data2 = loadFile('data/test2/data.json')
    data3 = loadFile('data/test5/data.json')
    data4 = loadFile('data/test6/data.json')
    data5 = loadFile('data/test7/data.json')
    data6 = loadFile('data/test3/data.json')
    data7 = loadFile('data/test12/data.json')
    #data8 = loadFile('data/test13.json')

    data_aut = loadFile('data/test_aut/data.json')
    proy_aut = data_aut['Nombre repositorio']
    comm_aut = data_aut['Commits totales']
    user_aut = data_aut['Contribuidores totales']

    #Preparing data
    data3 = parseDate(data3)
    data5 = parseDate(data5)
    data7 = parseDate(data7)

    # Loading it into gviz_api.DataTable
    data_table = createAndLoadDataTable(description,data)
    data_table2 = createAndLoadDataTable(description2,data2)
    data_table3 = createAndLoadDataTable(description3,data3)
    data_table4 = createAndLoadDataTable(description4,data4)
    data_table5 = createAndLoadDataTable(description5,data5)
    data_table6 = createAndLoadDataTable(description6,data6)
    data_table7 = createAndLoadDataTable(description7,data7)
    #data_table8 = createAndLoadDataTable(description8,data8)
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

    jscode7 = data_table7.ToJSCode("jscode7_data",
                                columns_order=("date","proy1", "proy2", "proy3"), 
                                order_by = "date")

    #jscode8 = data_table8.ToJSCode("jscode8_data",
    #                            columns_order=("inst","Parent", "commits"))

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