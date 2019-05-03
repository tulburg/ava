import sys

class Util: 

  def log(str, options=None) :
    if options != None :
      return print(str % (options))
    else :
      return print(str)

  def error(str, options=None) :
    if(options != None) :
      return print(str % (options), file=sys.stderr)
    else :
      return print(str)