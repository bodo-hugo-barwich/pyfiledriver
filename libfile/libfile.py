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
    
  
    if filepath is not None :
      self.setFilePath(filepath)
    else :
      if filedirectory is not None :
        self.setFileDirectory(filedirectory)
        
      if filename is not None :
        self.setFileName(filename)
  
   
  
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
      
      
  def _ropen(self):
    
    pass
  
  
  
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
      brs = True
      
    return brs