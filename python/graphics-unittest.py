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


if __name__ == "__main__":
    unittest.main()
