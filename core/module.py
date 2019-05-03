from core.util import Util
log = Util.log


class Module():

  def __init__(self) :
    self.__config = {
      'version': '0.0.1'
    }
    if not hasattr(self, "config") :
      raise NotImplementedError("Module configuration is required")
    if self.__validate() :
      pass

  def __validate(self) :
    if not self.config.get('name') :
      raise KeyError("Configuration file is invalid! 'name' is required")
      return False
    if not self.config.get("version") :
      raise KeyError("Configuration file is invalid! 'version' is required")
      return False
    if self.config.get("version") != self.__config.get("version") :
      raise SystemError(self.__class__.__name__+" module is not supported!")
    return True
  
