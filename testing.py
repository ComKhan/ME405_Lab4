import unittest

from sympy import interpolate
from hpproc import *



class Tests(unittest.TestCase):
    def test_ParseHPGL_1(self):
        instrList = parseHPGL('drawing.hpgl')
        self.assertEqual(instrList, [])

    def test_interpolate_1(self):
        instrList = [[0,0],[1,2], [1,3]]
        curnode = [0,1]
        resolution = 10
        print(interpolate(instrList, curnode, resolution))
        

if __name__ == '__main__':
    unittest.main()