#!/usr/bin/python
import unittest
import graphics
import os


class Test(unittest.TestCase):
    def testloadScheme(self):
        rootdir = os.path.join(os.getcwd(), "tests/schemas/")
        schema1 = {"user": ("string", "User name"),
                   "commits": ("number", "Number of user commits")}
        result1 = graphics.loadScheme(os.path.join(rootdir, 'schema1'))
        self.assertEqual(result1, schema1)
        schema2 = {'day': ('string', 'Day'),
                   'proy1': ('number', 'Commits proyecto 1'),
                   'proy2': ('number', 'Commits proyecto 2'),
                   'proy3': ('number', 'Commits proyecto 3')}
        result2 = graphics.loadScheme(os.path.join(rootdir, 'schema2'))
        self.assertEqual(result2, schema2)

    def testsetJScode(self):
        jscode = ''
        data = graphics.loadFile(os.path.join(os.getcwd(),
                                 "tests/data/test1/data.json"))
        description = graphics.loadScheme(os.path.join(os.getcwd(),
                                          "tests/data/test1/Autores"))
        contador = 0
        data_table = graphics.createAndLoadDataTable(
            description, data['Datos'])
        jscode = graphics.setJScode(
            jscode, data, data_table, contador, description)
        self.assertNotEqual(jscode.find(
          "jscode_data0.addColumn(\"string\", \"Nombre del autor\""), -1)
        self.assertNotEqual(jscode.find("jscode_data0.addRows(21);"), -1)
        self.assertNotEqual(jscode.find(
            "jscode_data0.setCell(2, 1, 0.6303724928366762);"), -1)
        contador += 1
        jscode = graphics.setJScode(
            jscode, data, data_table, contador, description)
        self.assertNotEqual(jscode.find(
            "jscode_data0.addColumn(\"string\", \"Nombre del autor\""), -1)
        self.assertNotEqual(jscode.find("jscode_data0.addRows(21);"), -1)
        self.assertNotEqual(jscode.find(
            "jscode_data0.setCell(2, 1, 0.6303724928366762);"), -1)
        self.assertNotEqual(jscode.find(
            "jscode_data1.addColumn(\"string\", \"Nombre del autor\""), -1)
        self.assertNotEqual(jscode.find("jscode_data1.addRows(21);"), -1)
        self.assertNotEqual(jscode.find(
            "jscode_data1.setCell(2, 1, 0.6303724928366762);"), -1)


if __name__ == "__main__":
    unittest.main()
