import re
from libs.states import state_object

class Intent(state_object) :

	def __init__(self, parentCls) :
		super(Intent, self).__init__()
		if not isinstance(parentCls, Intent) and not hasattr(parentCls, "__name__") :
			raise ValueError("Invalid parent class, parent class must be an intent")
		self.__name__ = parentCls.__name__ + ":" +str.lower(self.__class__.__name__)
		self.__dict__.update(self.get_state(self.__name__))

	def __setattr__(self, item, value) :
		super(Intent, self).__setattr__(item, value)
		if item != "__name__" :
			self.save(self.__name__)

	def start(self, state, stemma) :
		self.__dict__.update(self.get_state(self.__name__))
		
	def finish(self, state, stemma) :
		self.unpack()

	def pause(self, state, stemma) :
		self.save(self.__name__)

	def resume(self, state, stemma) :
		self.__dict__.update(self.get_state(self.__name__))

	def unpack(self) :
		self.__db_delete__(self.__name__)

	def stemmas() :
		intents = {
			"start" : "<<intent::start>>",
			"pause" : "<<intent::pause>>",
			"resume" : "<<intent::resume>>",
			"finish" : "<<intent::finish>>"
		}
		return state_object(**intents)


