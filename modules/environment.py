import os
from threading import Timer
from libs.utils import Logger
from intent import Intent

class Environment(Intent) :

	def __init__(self, manager, generator) :
		super(Environment, self).__init__(manager)
		self.manager = manager
		self.generator = generator
		self.manager.listen(self)

	def call(self, state, stemma) :
		getattr(self, stemma.stem(1))(state, stemma)
		# self.trigger("<<mind::start>>")

	def start(self, state, stemma) :
		log("got start on "+str(self.__class__))
		self.trigger(Intent.stemmas().start)
		super(Environment, self).start()

	def finish(self, state, stemma) :
		log("got stop on "+str(self.__class__))
		self.trigger(Intent.stemmas().finish)
		super(Environment, self).finish()

	def pause(self, state, stemma) :
		log("got pause on "+str(self.__class__))
		self.trigger(Intent.stemmas().pause)
		super(Environment, self).pause()

	def resume(self, state, stemma) :
		log("got resume on "+str(self.__class__))
		self.trigger(Intent.stemmas().resume)
		super(Environment, self)

	def intent(self, state, stemma) :
		speech = self.generator.speech("sorry([i][dont][understand]("+state["raw"]+"))")
		self.trigger(Intent.stemmas().finish)
	def respondent(self, state, stemma) :
		if stemma.stem(2) == "cantfindwithmac" :
			# speech = self.generator.speech("sorry")
			self.running = stemma.raw
			self.trigger(Intent.stemmas().finish)
		elif stemma.stem(2) == "unknown" :
			# speech = self.generator.speech("sorry([cant][remember](<<you>>))")
			# self.stop(state, stemma)
			self.trigger(Intent.stemmas().finish)

	def trigger(self, stemma) :
		self.manager.trigger(stemma)
	
log = Logger(Environment).log
