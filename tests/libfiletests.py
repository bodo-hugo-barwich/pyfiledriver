'''
Tests to verify the FileDriver Class Functionality

@version: 2019-06-01

@author: Bodo Hugo Barwich
'''
import sys
import unittest

sys.path.append("../libfile")

from libfile import FileDriver



class TestFileDriver(unittest.TestCase):


  _sfilename = "testfile.txt"


  def setUp(self):
    pass


  def tearDown(self):
    pass


  def test_Constructor(self):
    print("{} - go ...\n".format(sys._getframe().f_code.co_name))

    fl = FileDriver(None, None, self._sfilename)

    print("testConstructor - File Path: '{}'".format(fl.getFilePath()))
    print("testConstructor - File Directory: '{}'".format(fl.getFileDirectory()))
    print("testConstructor - File Name: '{}'".format(fl.getFileName()))

    self.assertEqual(fl.getFilePath()\
    , self._sfilename, "File Path is not built correctly.\n")
    self.assertEqual(fl.getFileDirectory()\
    , "", "File Directory is not empty.\n")
    self.assertEqual(fl.getFileName()\
    , self._sfilename, "File Name is not set correctly.\n")


  def test_FileExists(self):
    print("{} - go ...\n".format(sys._getframe().f_code.co_name))

    fl = FileDriver(None, None, self._sfilename)

    print("testFileExists - File Path: '{}'".format(fl.getFilePath()))

    self.assertEqual(fl.Exists()\
    , True, "Test File cannot be found.\n")



if __name__ == "__main__":
  print("tests starting ...\n")
  #import sys;sys.argv = ['', 'Test.testConstructor']
  unittest.main()

  print("tests done.\n")
