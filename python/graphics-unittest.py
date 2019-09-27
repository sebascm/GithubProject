#!/usr/bin/python
import graphics
import os


def testloadScheme(dir):
    scheme1 = {"user": ("string", "User name"),
               "commits": ("number", "Number of user commits")}
    result1 = graphics.loadScheme(os.path.join(dir, "schema1"))
    # Hecho rapido para que pep8 no de la lata
    if (scheme1 == result1):
        print "Bien"


def main():
    rootdir = os.path.join(os.getcwd(), "test/schemas")
    testloadScheme(rootdir)


if __name__ == "__main__":
    main()
