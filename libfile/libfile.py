'''
@version: 2018-10-22

@author: bodo
'''
from fileinput import filename

class FileDriver(object):
  '''
  classdocs
  '''


  def __init__(self, filepath = None, filedirectory = None, filename = None):
    '''
    Constructor
    '''
    self._file_path = ''
    self._file_directory = ''
    self._file_name = ''
  
  
   
  '''
  -----------------------------------------------------------------------------------------
  Administration Methods
  '''
  
      
  def setFileDirectory(self, filedirectory):
    if filedirectory is not None :
      self._file_directory = filedirectory
      
    if not self._file_directory.endswith('/', -1) :
      self._file_directory += '/'
      
  
  def setFileName(self, filename):
    if filename is not None :
      self._file_name = filename
      
    
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
    
    
    
    