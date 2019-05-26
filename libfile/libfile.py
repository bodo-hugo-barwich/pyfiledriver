'''
This Module provides the `FileDriver` Class which handles the Access to a Single
File implementing several functionalities in Python only Code and captures possible
Errors.

:version: 2018-10-27

:author: Bodo Hugo Barwich
'''
from __builtin__ import int
import os



class FileDriver(object):
  '''
  classdocs
  '''


  def __init__(self, filepath = None, filedirectory = None, filename = None):
    '''
    A `FileDriver` Object can be instanciate with a complete `filepath` or with
    `filedirectory` and / or `filename`
    '''
    self._arr_file_path = ['', '']
    self._file_path = None
    
    self._file = None
    self._arr_content = []
    self._arr_content_lines = []
    self._content = ''
    self._package_size = 32768
    self._cursor = -1
    self._persistent = False
    self._cached = False
    
    self._readable = False
    self._writeable = False
    self._appendable = False
    
    self._arr_err = []
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
  
   
  
  #-----------------------------------------------------------------------------------------
  #Administration Methods
    
      
  def setFileDirectory(self, filedirectory):
    if filedirectory is None :
      filedirectory = ''
    
    if filedirectory != '' :
      if not filedirectory.endswith('/', -1) :
        filedirectory += '/'
    
    self._file_path = None
    self._arr_file_path[0] = filedirectory
      
  
  def setFileName(self, filename):
    if filename is None :
      filename = ''
      
    self._file_path = None
    self._arr_file_path[1] = self._file_name
      
    
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
        filename = filepath[slashpos + 1 : filepath.length - 1]
      else :
        filedirectory = ''
        filename = filepath
        
    else :
      filedirectory = ''
      filename = ''
      
    self.setFileDirectory(filedirectory)
    self.setFileName(filename)
    
    
  def setPersistent(self, persistent = True):    
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
      
      
  def _rOpen(self, reopen = False):
    brs = False
    
    if not self._isOpen() or reopen :
      if self.Exists() :
        try :
          self._file = open(self.getFilePath(), 'rt', self._package_size)
        except Exception as e :
          self._file = None
          
          self._arr_err.append("File '{}': Open Read failed!".format(self.getFilePath()))
          self._arr_err.append("Message: {}".format(str(e)))
          self._err_code = 1
    else :
      brs = True
    
    return brs
  
  def Read(self):
    brs = False
    
    if not self._isReadable() :
      self._rOpen()
      
    if self._isOpen() :
      spk = None
      brd = True
    
      try :
        while brd :
          spk = self._file.read(self._package_size)
          
          if spk != '' :
            self._arr_content.append(spk)
          else :
            brd = False
            
        brs = True
        
      except Exception as e :
        self._arr_err.append("File '{}': Read failed!".format(self.getFilePath()))
        self._arr_err.append("Message: {}".format(str(e)))
        self._err_code = 1
        
        self._Close()
        
      if not self._persistent :
        #Close the File in non persistent Mode
        self._Close()
        
    return brs
  
  
  def _Close(self):
    if self._isOpen() :
      self._file.close()
      self._file = None
      
    self._readable = False
    self._writeable = False
    self._appendable = False
  
  
  
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
  
  
  def Exists(self):
    brs = os.path.exists(self.getFilePath())
    
    if brs :
      brs = os.path.isfile(self.getFilePath())
        
    return brs
  
  
  def _isOpen(self):
    brs = False
    
    if self._file is not None :
      try :
        if self.file.fileno() != 0 :         
          brs = True
        else :
          #It is not a valid File Object
          self._file = None      
          self._readable = False
          self._writeable = False
          self._appendable = False          
      except :
        #It is not a valid File Object
        self._file = None      
        self._readable = False
        self._writeable = False
        self._appendable = False
            
    return brs
  
  
  def _isReadable(self):
    brs = False
    
    if self._isOpen() and self._readable :
      brs = True
      
    return brs
  
  
  def _isWriteable(self):
    brs = False
    
    if self._isOpen() and self._writeable :
      brs = True
      
    return brs