import ast
from data.db import states
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(config.db_connector+"://"+config.db_username+":"+config.db_password+"@"+config.db_hostname+":"+config.db_port+"/"+config.db_name)
conn = engine.connect()
Session = sessionmaker(bind=engine)
db = Session()

class state_object(dict) :

	def __init__(self, **entries) :
		self.__dict__.update(entries)
		dict.__init__(self, entries)
		for key in entries :
			if isinstance(entries[key], dict) :
				self.__setattr__(key, entries[key])

	def __setattr__(self, item, value) :
		if isinstance(value, dict):
			_value = self[item] = state_object(**value)
			self.__dict__.update({item : _value})
		else :
			_value = self[item] = value
			self.__dict__.update({item : _value})

	def save(self, dbid) :
		state = db.query(states).filter_by(id=dbid).first()
		prop = {}
		for a in self.__dict__ :
			opts = (float,int,str,tuple,dict,list,bool,None)
			for t in opts :
				if type(self.__dict__[a]) is t :
					prop.update({a:self.__dict__[a]})
					break
				else :
					prop.update({a:str(self.__dict__[a])})
					break
			# -- todo: big issue here, don't know how to solve yet
			# -- trying to avoid ast.literal_eval crash during get_state()
			# if self.__dict__[a] != None and isinstance(self.__dict__[a], opts) :
		if state != None :
			state.state = str(prop)
		else :
			add = states(id=dbid, state=str(prop))
			db.add(add)
		db.commit()

	def get_state(self, dbid) :
		state = db.query(states).filter_by(id=dbid).first()
		if state != None :
			return ast.literal_eval(state.state)
		return {}
		

	def __db_delete__(self, dbid) :
		db.query(states).filter_by(id=dbid).delete()
		db.commit()
		
	def from_string(str) :
		e = ast.literal_eval(str)
		return state_object(**e)
