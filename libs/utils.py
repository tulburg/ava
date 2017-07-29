import time
from collections import namedtuple
from uuid import getnode as get_mac
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.db import entities, db_utils


engine = create_engine(config.db_connector+"://"+config.db_username+":"+config.db_password+"@"+config.db_hostname+":"+config.db_port+"/"+config.db_name)
conn = engine.connect()
Session = sessionmaker(bind=engine)
db = Session()

class MObject:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class util :
	@staticmethod
	def dict_to_obj(dicti) :
		"""
		Converts dictionaries to class objects
		"""
		return MObject(**dicti)
	@staticmethod
	def name_to_alias(name = 'user') :
		names = db.query(entities).filter_by(name=name).first()
		if names != None :
			return name+"_"+db_utils.get_id(entities)
		return name
		
	@staticmethod
	def mac_address() :
		return get_mac()

	def match(a, b) :
		if a.__contains__("...") :
			i = a.index("...")
			if i == 0 :
				aa = a[3:]
				if aa.__contains__("...") :
					aa = aa[:-3]
					if b.__contains__(aa) and b.index(aa) != 0 and b.index(aa) != len(b[:-len(aa)]):
						pro = (len(aa.split(" ")) + len(Parser.profilers(aa))) / (len(b.split(" ")) + len(Parser.profilers(b)))
						return (True, pro)
					else :
						pro = (len(aa.split(" ")) + len(Parser.profilers(aa))) / (len(b.split(" ")) + len(Parser.profilers(b)))
						return (False, pro)
				elif b.__contains__(aa) :
					pro = (len(aa.split(" ")) + len(Parser.profilers(aa))) / (len(b.split(" ")) + len(Parser.profilers(b)))
					if b.__contains__(aa) and b.index(aa) == len(b[:-len(aa)]):
						return (True, pro)
					else :
						return (False, pro)
			elif i == len(a[:-3]) :
				aa = a[:-3]
				pro = (len(aa.split(" ")) + len(Parser.profilers(aa))) / (len(b.split(" ")) + len(Parser.profilers(b)))
				if b.__contains__(aa) and b.index(aa) == 0:
					return (True, pro)
				else :
					return (False, pro)
		else :

			pro = (len(a.split(" ")) + len(Parser.profilers(a))) / (len(b.split(" ")) + len(Parser.profilers(b)))
			if b.__contains__(a) and b.index(a) != len(b[:-len(a)]):
				return (True, pro)
			else :
				return (False, pro)

class stemmas :
	def __init__(self, string) :
		res = {}
		self.__raw__ = string
		string = string[2:-2]
		self.index = 0
		first_split = string.split("::")
		second_split = string.split(":")
		if len(first_split) > 1 :
			self.split = first_split
			self.__type__ = "double"
		elif len(second_split) > 0 :
			self.split = second_split
			self.__type__ = "single"
		self.root = self.split[self.index]
		self.raw = self.__raw__
	def stem(self, at = 1) :
		return self.split[at]
		# sets = dict(zip(keys, split))

class Logger() :
	def __init__(self, cls) :
		self.name = cls.__name__

	def log(self, msg) :
		print(time.strftime("%F %I:%M:%S")+" "+self.name+" :: "+msg)
