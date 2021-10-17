'''
This Module provides the `FileDriver` Class which handles the Access to a Single
File implementing several functionalities in Python only Code and captures possible
Errors.

:version: 2020-07-11

:author: Bodo Hugo Barwich
'''
__docformat__ = "restructuredtext en"

import os
import sys
from io import FileIO
from io import SEEK_SET


class FileDriver(object):
  '''
  This is a Class to interact with a physical Text File in a easy and convenient way.

  It offers Methods read and write from and to the File
  '''


  #----------------------------------------------------------------------------
  #Constructors


  def __init__(self, filepath = None, filedirectory = None, filename = None):
    '''
    A `FileDriver` Object can be instantiated with a complete `filepath` or with
    `filedirectory` and / or `filename`
    '''
    self._arr_file_path = ['', '']
    self._file_path = None

    self._file = None
    self._arr_content = []
    self._arr_content_lines = []
    self._scontent = ''
    self._package_size = 32768 # 16 #
    self._icursor = -1
    self._persistent = False
    self._cached = False

    self._breadable = False
    self._bwriteable = False
    self._bappendable = False

    self._arr_rpt = []
    self._arr_err = []
    self._sreport = None
    self._serror = None
    self._err_code = 0

    if filepath is not None :
      self.setFilePath(filepath)
    else :
      if filedirectory is not None :
        self.setFileDirectory(filedirectory)

      if filename is not None :
        self.setFileName(filename)


  def __del__(self):
    '''
    On Destruction the File will be closed
    and the Lists of str Objects will be freed
    '''
    if self._isOpen() :
      self._Close()

    self._arr_content = None
    self._arr_content_lines = None

    self._arr_rpt = None
    self._arr_err = None



  #-----------------------------------------------------------------------------------------
  #Administration Methods


  def setFileDirectory(self, filedirectory):
    '''
    This Method sets the directory of the file.
    If the directory does not end with a slash "/" it will be added

    :param filedirectory: The Directory of the File
    :type filedirectory: string
    '''
    #Reset former cached File Path
    self._file_path = None
    self._arr_file_path[0] = ''

    if filedirectory is None :
      filedirectory = ''

    if filedirectory != '' :
      if not filedirectory.endswith('/', -1) :
        self._arr_file_path[0] = filedirectory + '/'
      else :
        self._arr_file_path[0] = filedirectory


  def setFileName(self, filename):
    if filename is None :
      filename = ''

    #Reset former cached File Path
    self._file_path = None
    self._arr_file_path[1] = filename


  def setFilePath(self, filepath):
    filedirectory = None
    filename = None
    slashpos = -1

    if filepath is None :
      filepath = ''

    self._file_path = filepath

    if filepath != '' :
      slashpos = filepath.rfind('/', 0)

      if slashpos != -1 :
        filedirectory = filepath[0 : slashpos]
        filename = filepath[slashpos + 1 : len(filepath) - 1]
      else :
        filedirectory = ''
        filename = filepath

    else :
      filedirectory = ''
      filename = ''

    self.setFileDirectory(filedirectory)
    self.setFileName(filename)


  def setPersistent(self, persistent = True):
    '''
    This Method enables the Persistence feature.
    With the Persistence feature the File will not be closed after each Read action.
    This enables the File to be read in Chunks

    :param persistent: Whether the Persistence feature to be enabled
    :type persistent: boolean
    '''
    if isinstance(persistent, int) :
      if persistent > 0 :
        persistent = True
      else :
        persistent = False

    if isinstance(persistent, bool) :
      self._persistent = persistent


  def setCached(self, cached = True):
    if isinstance(cached, int) :
      if cached > 0 :
        cached = True
      else :
        cached = False

    if isinstance(cached, bool) :
      self._cached = cached


  def setContent(self, scontent):
    if scontent is None :
      scontent = ''

    self._scontent = scontent


  def _rOpen(self, reopen = False):
    brs = False

    if not self._isReadable() :
      self._Close()

    if not self._isOpen() or reopen :
      if self.Exists() :
        try :
          self._file = FileIO(self.getFilePath(), 'r')

          self._file._blksize = self._package_size

          #Reset the File Cursor
          self._file.seek(SEEK_SET)

          self._breadable = self._file.readable()

          #No Exception has occurred
          brs = True

        except Exception as e :
          self._file = None

          #Reset the internal File Status
          self._Close()

          self._arr_err.append("File '{}': Open Read failed!".format(self.getFilePath()))
          self._arr_err.append("Message: {}".format(str(e)))
          self._err_code = 1

    else :
      brs = True

    return brs


  def _wOpen(self):
    brs = False

    if not self._isWriteable() :
      self._Close()

    if not self._isOpen() :
      if self.Exists() :
        try :
          try :
            self._file = FileIO(self.getFilePath(), 'w')
          except FileExistsError as e :
            #Ignore the File does already exists Exception
            pass

          if self._isOpen() :
            self._file._blksize = self._package_size
            self._bwriteable = self._file.writable()
            #No Exception has occurred
            brs = True

        except Exception as e :
          self._file = None

          #Reset the internal File Status
          self._Close()

          self._arr_err.append("File '{}': Open Write failed!".format(self.getFilePath()))
          self._arr_err.append("Message: {}".format(str(e)))
          self._err_code = 1

      else :
        #A valid Directory is required
        if self.DirectoryExists() :
          try :
            self._file = FileIO(self.getFilePath(), 'w')

            self._file._blksize = self._package_size

            self._bwriteable = self._file.writable()
          except Exception as e :
            self._file = None

            #Reset the internal File Status
            self._Close()

            self._arr_err.append("File '{}': Open Write failed!".format(self.getFilePath()))
            self._arr_err.append("Message: {}".format(str(e)))
            self._err_code = 1
    else :
      brs = True

    return brs


  def Read(self):
    brs = False

    #Clear previous Errors
    self.clearErrors()

    if not self._isReadable() :
      self._rOpen(True)

    if self._isOpen() :
      scnk = None
      brd = True

      #Reset the Content Buffer
      self._scontent = None

      try :
        while brd :
          scnk = self._file.read(self._package_size)

          print("got chunk: '{}'".format(str(scnk, sys.stdout.encoding)))

          if scnk is not None :
            scnk = str(scnk, sys.stdout.encoding)

            if scnk != '' :
              self._arr_content.append(scnk)
            else :
              brd = False
          else :
            brd = False

        if scnk is not None :
          #File was read without Exception
          brs = True

      except Exception as e :
        self._arr_err.append("File '{}': Read failed!".format(self.getFilePath()))
        self._arr_err.append("Message: {}".format(str(e)))
        self._err_code = 1

        #Close the File because of an Error
        self._Close()

      if not self._persistent :
        #Close the File in non persistent Mode
        self._Close()

    return brs


  def Write(self):
    brs = False

    #Clear previous Errors
    self.clearErrors()

    if not self._isWriteable() :
      self._wOpen()

    if self._isOpen() :
      #Build the Content String
      arrcntnt = bytes(self.getContent(), sys.stdout.encoding)
      icntntln = len(arrcntnt)
      iwrtstrt = 0
      iwrtend = self._package_size if icntntln > self._package_size else icntntln
      iwrtcnt = -1
      iwrtttlcnt = -1

      bwrt = True

      try :
        while bwrt and iwrtttlcnt < icntntln :
          iwrtcnt = self._file.write(arrcntnt[iwrtstrt : iwrtend])

          if iwrtcnt is not None :
            if iwrtttlcnt == -1 :
              iwrtttlcnt = iwrtcnt
            else :
              iwrtttlcnt += iwrtcnt

            if iwrtttlcnt < icntntln :
              iwrtstrt = iwrtttlcnt
              iwrtend = iwrtstrt

            if iwrtend < icntntln :
              iwrtend = iwrtend + self._package_size if icntntln - iwrtend > self._package_size else icntntln
            else :
              bwrt = False

          else :
            bwrt = False

        if iwrtttlcnt != icntntln :
          self._arr_err.append("File '{}': Write failed!".format(self.getFilePath()))
          self._arr_err.append("Message: Written Only ({} / {}) Bytes.".format([iwrtcnt, icntntln]))
          self._err_code = 1

          #Close the File because of an Error
          self._Close()

        else :  #Content was written correctly
          brs = True

      except Exception as e :
        self._arr_err.append("File '{}': Write failed!".format(self.getFilePath()))
        self._arr_err.append("Message: {}".format(str(e)))
        self._err_code = 1

        #Close the File because of an Error
        self._Close()

      if not self._persistent :
        #Close the File in non persistent Mode
        self._Close()

    return brs



  def readChunk(self):
    brs = False

    if not self._isReadable() :
      self._rOpen(True)

    if self._isOpen() :
      scnk = None
      brd = True

      #Reset the Content Buffer
      self._scontent = None

      try :
        scnk = self._file.read(self._package_size)

        if scnk != '' :
          self._arr_content.append(scnk)
        else :
          brd = False

        #File was read without Exception
        brs = True

      except Exception as e :
        self._arr_err.append("File '{}': Read failed!".format(self.getFilePath()))
        self._arr_err.append("Message: {}".format(str(e)))
        self._err_code = 1

        #Close the File because of an Error
        self._Close()

      if not brd and not self._persistent :
        #Close the File in non persistent Mode
        self._Close()

    return brs


  def readContent(self):
    self.Read()

    return self.getContent()


  def writeContent(self, scontent):
    self.setContent(scontent)

    return self.Write()


  def readLine(self):
    pass


  def clearErrors(self):
    self._arr_rpt = []
    self._arr_err = []
    self._sreport = None
    self._serror = None
    self._err_code = 0


  def _Close(self):
    if self._isOpen() :
      self._file.close()
      self._file = None

    self._icursor = -1
    self._breadable = False
    self._bwriteable = False
    self._bappendable = False



  #-----------------------------------------------------------------------------------------
  #Consultation Methods


  def getFileDirectory(self):
    return self._arr_file_path[0]


  def getFileName(self):
    return self._arr_file_path[1]


  def getFilePath(self):
    if self._file_path is None :
      self._file_path = ''.join(self._arr_file_path)

    return self._file_path


  def getContent(self):
    if self._scontent is None :
      self._scontent = ''.join(self._arr_content)

    return self._scontent


  def getLine(self):
    pass


  def DirectoryExists(self):
    brs = False

    #An empty Directory is the current Working Directory
    if self.getFileDirectory() != '' :
      brs = os.path.exists(self.getFileDirectory())
    else :
      brs = True

    return brs


  def Exists(self):
    #Check the Directory first
    brs = self.DirectoryExists()

    #File Name must be set
    if brs and self.getFileName() != '' :
      brs = os.path.exists(self.getFilePath())
    else :
      brs = False

    return brs


  def getReportString(self):
    if self._sreport is None :
      self._sreport = "\n".join(self._arr_rpt)

    return self._sreport


  def getErrorString(self):
    if self._serror is None :
      self._serror = "\n".join(self._arr_err)

    return self._serror


  def getErrorCode(self):
    return self._err_code


  def _isOpen(self):
    brs = False

    if self._file is not None :
      try :
        if self._file.fileno() > 0 :
          brs = True
        else :
          #It is not a valid File Object
          self._file = None
          self._icursor = -1
          self._readable = False
          self._writeable = False
          self._appendable = False
      except :
        #It is not a valid File Object
        self._file = None
        self._icursor = -1
        self._readable = False
        self._writeable = False
        self._appendable = False

    return brs


  def _isReadable(self):
    brs = False

    if self._isOpen() and self._breadable :
      brs = True

    return brs


  def _isWriteable(self):
    brs = False

    if self._isOpen() and self._bwriteable :
      brs = True

    return brs


  def _isAppendable(self):
    brs = False

    if self._isOpen() and self._bappendable :
      brs = True

    return brs

