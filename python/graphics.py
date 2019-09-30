#!/usr/bin/python3
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
        data[i]['date'] = datetime.datetime.strptime(
            data[i]['date'], '%Y-%m-%d')
    return data


def createAndLoadDataTable(description, data):
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    return data_table


def loadScheme(file):
    with open(file, 'r') as f:
        s = f.read()
        return ast.literal_eval(s)


def setJScode(jscode, data, data_table, contador, description):
    if 'Ordenacion' in data:
        jscode = jscode + '\n' + data_table.ToJSCode(
            "jscode_data" + str(contador), columns_order=(
                description.keys()), order_by=str(
                data['Ordenacion']))
    else:
        jscode = jscode + '\n' + data_table.ToJSCode(
            "jscode_data" + str(contador), columns_order=(
                description.keys()))
    return jscode


def main():
    jscode = ''
    ejecucion = ''
    opciones = ''
    divs = ''
    contador = 0
    rootdir = os.path.join(os.getcwd(), "data/")

    for subdir, dirs, files in os.walk(rootdir):
        data = None
        description = None
        for file in files:
            archivo = os.path.join(subdir, file)
            if file == 'data.json':
                data = loadFile(archivo)
                if 'date' in data:
                    data = parseDate(data)
                description = loadScheme(os.path.join(
                    rootdir, 'schemas/' + str(data['Tipo'])))
        if data is not None:
            data_table = createAndLoadDataTable(description, data['Datos'])
            grafico = str(data['Grafico']) + '_' + str(contador)
            divs = divs + 'var iDiv = document.createElement(\'div\'); ' \
                + '\n' + 'iDiv.id = \'' + grafico + '_div\';' + '\n' + \
                'document.getElementsByTagName(\'body\')[0].appendChild(iDiv);'
            ejecucion = ejecucion + '\n' + 'var chart_' + grafico + \
                '= new google.visualization.' + str(data['Grafico']) + \
                '(document.getElementById(\'' + grafico + '_div\'));'
            opciones = opciones + '\n' + 'chart_' + grafico + \
                '.draw(jscode_data' + str(contador) + ',' + \
                str(data['Grafico']) + '_options);'
            jscode = setJScode(jscode, data, data_table, contador, description)
        contador += 1

    pagina = page_template % vars()
    if not os.path.isdir("generated"):
        os.mkdir("generated")
    f = open("generated/prueba.html", "w+")
    f.write(pagina)
    f.close()


if __name__ == "__main__":
    main()
