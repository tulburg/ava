import os, sys, time
from threading import Timer
from multiprocessing import Process
from predict import Predict
from libs.utils import stemmas, Logger
from data.db import states
from libs.states import state_object
from intent import Intent


class Manager(Process) :
	def __init__(self, queue):
		super(Manager, self).__init__()
		self.load()
		self.__name__ = "manager"
		self._queue = queue
		self.running = True
		self.intent_queue = {}
		self.idle_timer = Timer(5, self.idle) # timer before feeling bored

	def get(self) :
		return self._queue.get()

	def update(self, state) :
		self.load()
		self.state.conversation.append(state)
		self.save()

	def run(self) :
		while(self.running) :
			msg = self._queue.get()
			# log("\"\" "+str(self.intent_queue))
			if msg != None :
				if msg.root == "manager" :
					if msg.stem(1) == "start" :
						self.trigger("<<mind::start>>")
					elif msg.stem(1) == "stop" :
						print("\"\" mind stopped...")
						self.running = False
					elif msg.stem(1) == "idle" :
						# log("i'm idle")
						_ = True
					elif msg.stem(1) == "update" :
						_ = True
					elif msg.stem(1) == "nullintent" :
						if self.is_running() :
							intent = stemmas(self.state.running)
							self.intent_queue[intent.root].call(self.state.conversation[-1], intent)
						else :
							self.trigger("<<environment:intent:nullintent>>")
						# self.state = state_object.from_string(msg.stem(2))
				elif self.intent_queue.keys().__contains__(msg.root) :
					self.load()
					if len(self.state.conversation) > 0 :
						self.intent_queue[msg.root].call(self.state.conversation[-1], msg)
					else :
						self.intent_queue[msg.root].call({}, msg)
					# p.start()
					# self.trigger(self.intents.start)
				else :
					self.trigger(msg.raw)
					# print("\"\" unknown intent :: "+ msg.raw)
			time.sleep(1)
	
	def listen(self, cls) :
		self.intent_queue.update({str.lower(cls.__class__.__name__) : cls})
	
	def trigger(self, event, interrupt = False) :
		ex = ["mind", "intent", "manager"]
		msg = stemmas(event)
		# log(msg.raw)
		if msg.root == "intent" :
			if msg.stem(1) == "start" :
				_ = True
			elif msg.stem(1) == "finish" :
				# log("got finished for "+str(self.get_running()))
				self.set_running("")
				self.next()
				self.trigger("<<mind::start>>")
			elif msg.stem(1) == "pause" :
				p = Process(target=self.intent_queue[self.current_intent_root].pause, args=(self.state, msg))
				p.start()
				# self.set_paused(msg.raw)
			elif msg.stem(1) == "resume" :
				_ = True
				# self.set_paused("")
		elif self.is_running() == True and interrupt != True and ex.__contains__(stemmas(event).root) == False:
				self.add_pre_queue(event)
				# log("Can't run "+event+" -> still running process "+ self.get_running())
				# log(str(self.get_pre_queue()))
		else :
			if ex.__contains__(stemmas(event).root) == False:
				self.trigger(Intent.stemmas().start)
				self.current_intent_root = stemmas(event).root
				self.set_running(event)
				# log("set running for "+event)
			if interrupt :
				self._queue.put(stemmas(Intent.stemmas().pause))
				self.set_paused(self.get_running())
			self._queue.put(stemmas(event))
	
	def next(self) :
		self.load()
		self.idle_timer.cancel()
		if len(self.get_pre_queue()) > 0 and self.is_running() == False :
			self.trigger(self.get_pre_queue()[-1])
			self.state.pre_queue = self.get_pre_queue()[:-1]
			self.save()
		else :
			# self.trigger("<<mind::start>>")
			# log(str(self.state))
			self.idle_timer = Timer(5, self.idle)
			self.idle_timer.start()

	def idle(self) :
		self._queue.put(stemmas("<<manager::idle>>"))

	def add_pre_queue(self, intent) :
		self.load()
		self.state.pre_queue.append(intent)
		self.save()
	def get_pre_queue(self) :
		self.load()
		return self.state.pre_queue
	def set_running(self, intent) :
		self.load()
		self.state.running = intent
		self.save()
	def set_paused(self, intent) :
		self.load()
		self.state.paused = intent
		self.save()
	def get_running(self) :
		self.load()
		return self.state.running
	def get_paused(self) :
		self.load()
		return self.state.paused
	def is_running(self) :
		self.load()
		return self.state.running != ""
	def is_paused(self) :
		self.load()
		return self.state.paused != ""
	def unpack(self) :
		log("Manager unpacked")
		self.running = False
		self.state = {
			"running" : "",
			"paused" : "",
			"conversation" : [],
			"pre_queue" : [],
			"entities" : []
		}
		self.save()

	def load(self) :
		try :
			with open("data/.shared_state", "r") as f :
				r = f.readline()
				self.state = state_object.from_string(r)
		except Exception as e:
			print(e.error)

	def save(self) :
		with open("data/.shared_state", "w") as f :
			if hasattr(self, 'state') :
				f.write(str(self.state))




log = Logger(Manager).log


	