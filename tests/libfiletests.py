'''
Tests to verify the FileDriver Class Functionality

@version: 2019-06-01

@author: Bodo Hugo Barwich
'''
import sys
import unittest
import os

sys.path.append("../libfile")

from libfile import FileDriver



class TestFileDriver(unittest.TestCase):


  _sfilename = "testfile.txt"


  def setUp(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))
    print("setUp - Test Directory: '{}'".format(os.getcwd()))
    print("setUp - Test Module: '{}'\n".format(__file__))
    print("")


  def tearDown(self):
    pass


  def test_Constructor(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

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

    print("")


  def test_FileExists(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    #Get the Working Directory from the Module File Name
    fl = FileDriver(__file__)

    #Override the Module File Name with the actual Test File
    fl.setFileName(self._sfilename)

    print("testFileExists - File Path: '{}'".format(fl.getFilePath()))

    self.assertEqual(fl.Exists()\
    , True, "Test File cannot be found.\n")

    print("")


  def test_FileRead(self):
    print("{} - go ...".format(sys._getframe().f_code.co_name))

    #Get the Working Directory from the Module File Name
    fl = FileDriver(__file__)

    #Override the Module File Name with the actual Test File
    fl.setFileName(self._sfilename)

    print("testFileExists - File Path: '{}'".format(fl.getFilePath()))

    if fl.Exists() :
      self.assertEqual(fl.Read()\
      , True, "Test File cannot be found.\n")
      self.assertFalse(fl.getContent() == '' \
      , "Test File was not read correctly.\n")
    else :
      self.assertEqual(fl.Exists()\
      , True, "Test File cannot be found.\n")

    print("")



if __name__ == "__main__":
  print("test module: '{}'".format(__file__))

  print("tests starting ...\n")
  #import sys;sys.argv = ['', 'Test.testConstructor']
  unittest.main()

  print("tests done.\n")
