'''
Tests to verify the FileDriver Class Functionality

@version: 2019-06-01

@author: Bodo Hugo Barwich
'''



import sys
import unittest

sys.path.append("../libfile")

from liblog import FileDriver


class TestFileDriver(unittest.TestCase):

  def setUp(self):
    pass


  def tearDown(self):
    pass




if __name__ == "__main__":
  print("tests starting ...\n")
  #import sys;sys.argv = ['', 'Test.testConstructor']
  unittest.main()

  print("tests done.\n")
