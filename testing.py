import unittest

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

    def test_instr_conv1(self):
        instrList = ['PD', '25', '30', '40', '52']
        self.assertEqual(instrconv(instrList), [[25, 30], [40, 52]])

    def test_instr_conv2(self):
        instrList = ['PD', '25', '30', '40', '-52']
        self.assertEqual(instrconv(instrList), [[25, 30], [40, -52]])

    def test_instr_conv2(self):
        instrList = ['PU', '25', '30', '40', '-52']
        self.assertEqual(instrconv(instrList), [[25, 30], [40, -52]])

        

if __name__ == '__main__':
    unittest.main()