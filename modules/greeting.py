import os
from threading import Timer
from libs.utils import Logger

class Greeting :

	def __init__(self, manager, generator) :
		self.manager = manager
		self.generator = generator
		self.manager.listen(self)

	def call(self, state, stemma) :
		getattr(self, stemma.stem(1))(state, stemma)

	def pause(self, state, stemma) :
		log("got pause on "+str(self.__class__))

	def play(self, state, stemma) :
		log("got continue on "+str(self.__class__))

	def casual(self, state, stemma) :
		if stemma.stem(2) == "hi" :
			speech = self.generator.speech("hi")
			log(speech)
		elif stemma.stem(2) == "hello" :
			speech = self.generator.speech("hello")
			log(speech)

log = Logger(Greeting).log