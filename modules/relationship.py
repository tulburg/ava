from libs.utils import Logger, util
from intent import Intent

class Relationship(Intent) :

	def __init__(self, manager, generator) :
		super(Relationship, self).__init__(manager)
		self.manager = manager
		self.generator = generator
		self.manager.listen(self)
		#

	def greeting(self, state, stemma) :
		# 1. Read memory
		# 2. Fetch relationship status
		# log(str(state))
		log("Hey, how are you?")
		if state["raw"] == "okay" :
			self.trigger(Intent.stemmas().finish)
		else :
			# self.trigger(Intent.stemmas().finish)
			self.trigger("<<mind::start>>")


	def call(self, state, stemma) :
		getattr(self, stemma.stem(1))(state, stemma)

	def start(self, state, stemma) :
		log("got start on "+str(self.__class__))
		self.trigger(Intent.stemmas().start)
		super(Environment, self).start()

	def finish(self, state, stemma) :
		log("got stop on "+str(self.__class__))
		self.trigger(Intent.stammas().finish)
		super(Environment, self).finish()

	def pause(self, state, stemma) :
		log("got pause on "+str(self.__class__))
		self.trigger(self.stemmas().pause)
		super(Environment, self).pause()

	def resume(self, state, stemma) :
		log("got resume on "+str(self.__class__))
		self.trigger(self.stemmas().resume)
		super(Environment, self)

	def trigger(self, stemma) :
		self.manager.trigger(stemma)

log = Logger(Relationship).log


