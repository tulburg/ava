import os, sys, re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.db import entities, props, states, matrix, config
from normalizer import Normalize
from parser import Parser
from libs.utils import util, Logger
from libs.states import state_object


# initializations
engine = create_engine(config.db_connector+"://"+config.db_username+":"+config.db_password+"@"+config.db_hostname+":"+config.db_port+"/"+config.db_name)
conn = engine.connect()
Session = sessionmaker(bind=engine)
db = Session()

class Mind :
	def __init__(self, manager, fn) :
		self._manager = manager
		self.ref = "1x0"
		self.respondent = None
		self.run = True
		self.temp = []
		self.liege = db.query(entities).filter_by(id="0x2").first()
		self.start(fn)
		self.load()

	def trigger(self, event, globally = False) :
		self._manager.trigger(event)
		# Todo: Setup a global queue for messages
		# meant for global applications

	def acquire_respondent(self, key="mac", value=util.mac_address()) :
		user = props.get_by_rel(key, value)
		if len(user) < 1 :
			chaking = True
			if key == "mac" :
				self.trigger("<<environment:respondent:cantfindwithmac>>", globally=True)
			else : 
				self.trigger("<<environment:respondent:cantfindwith"+key+">>", globally=True)
			# self.trigger("<<request:user:name>>")
		elif len(user) == 1 :
			u = props.get(user[0].ref)
			self.respondent = state_object(u)
			return self.respondent
		else :
			return None

	def start(self, fn) :
		self.trigger("<<manager::start>>")
		sys.stdin = os.fdopen(fn)
		while(self.run) :
			msg = self._manager.get()
			if msg.root == "mind" :
				if msg.stem(1) == "start" :
					self.run = True
					sen = str(input(">> "))
					if sen != "" :
						respondent = self.acquire_respondent()

						expanded = Normalize.expand(sen)
						lemmanized = Normalize.lemmanize(expanded)
						entities = Parser.entities_alt(lemmanized)
						# entitized = self.cast_entities(entities)

						conv = state_object()
						conv.subjects = []
						conv.raw = sen
						conv.parsed = lemmanized
						# for k, v in entitized.items() :
						# 	conv.subjects.append(v)
						# 	lemmanized = re.sub(k, v, lemmanized)
						objects = Parser.entities(lemmanized)
						objectized = self.cast_objects(objects)
						self.load()
						for k, v in objectized.items() :
							self.state.entities.append(v)
							lemmanized = re.sub(k, v, lemmanized)
						# subjs.respondent = 
						# conv.
						self.state.conversation.append(conv)
						self.save()
						# log(str(entitized))
						# log(str(objectized))

						# log(lemmanized)
						# self.trigger("<<manager::update::"+str(conv)+">>")

						if respondent == None :
							self.trigger("<<environment:respondent:unknown>>")

						m = matrix.get(lemmanized)
						if len(m) == 1 :
							self.trigger(m[0].value)
						else :
							self.trigger("<<manager::nullintent>>")
						# self.trigger("<<mind::start>>")
						""" Process
						- first we extract the skeleton of the sentence structure
						  and its subjects for the matrix
						- second we parse the parameters and the relationships for
						  the data tree (entities and props)
						- third we match the extracted skeleton of the sentence
						  structrue with respective action and call it
						- fourth we add the collection of successive matrix calls
						  to the matrix
						"""
				elif msg.stem(1) == "stop" :
					log("ava stopped")
					self.run = False
				elif msg.stem(1) == "listen" :
					self.trigger("<<mind::start>>")
			else :
				self.trigger(msg.raw)
				# message("not for me " +msg.raw)
				

	def cast_entities(self, entities) :
		ex_entities = self.state.entities
		# respondent = self.respondent.ref
		respondent = "self"
		res = []
		for e in entities :
			e = e[2:-2]
			if e == "me" or e == "i" :
				res.append("<<"+respondent+">>")
			elif e == "you" :
				res.append("<<"+self.ref+">>")
			elif e == "it" or "itself" :
				# not right, this is a placeholder
				# need to search subjects to find
				# a match for the type referenced
				res.append("<<"+ex_entities[0].id+">>")
		return dict(zip(entities, res))

	def cast_objects(self, entities) :
		res = []
		for i in range(len(entities)) :
			ent = entities[i]
			ent = ent[1:-1]
			if ent.split(" ")[0] == "my" :
				ent = re.sub("my ", "<<"+self.respondent.ref+">>-", ent)
			elif ent.split(" ")[0] == "your" :
				ent = re.sub("your ", "<<"+self.ref+">>-", ent)
			# elif ent.split(" ")[0][-2] == "'s" :
			# 	named = ent.split(" ")[0][:-2]
			else :
				prop = props.get_by_name(ent)
				if prop != None :
					ent = "<<"+prop.ref+">>"
				else :
					a = True
					# ent = "<<unknown>>"

			res.append("{"+ent+"}")
		return dict(zip(entities, res))

	def __get_state__(self) :
		return util.dict_to_obj(self.state) 

	def load(self) :
		with open("data/.shared_state", "r") as f :
			r = f.readline()
			self.state = state_object.from_string(r)

	def save(self) :
		with open("data/.shared_state", "w") as f :
			if hasattr(self, 'state') :
				f.write(str(self.state))

log = Logger(Mind).log
