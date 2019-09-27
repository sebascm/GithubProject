#!/usr/bin/python
import graphics
import os

class TestSum(unittest.TestCase):

	def testloadScheme(dir):
		scheme1 = { "user": ("string", "User name"),
	    	            "commits": ("number", "Number of user commits")}
		result1 = graphics.loadScheme(os.path.join(dir, "schema1"))
		assertEqual(result1, scheme1)

def main():
	rootdir = os.path.join(os.getcwd(), "test/schemas")
	testloadScheme(rootdir)

if __name__ == "__main__":
    main()