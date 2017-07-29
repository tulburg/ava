from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, create_engine, func
from sqlalchemy.orm import sessionmaker

from data.config import *

Base = declarative_base()

engine = create_engine(config.db_connector+"://"+config.db_username+":"+config.db_password+"@"+config.db_hostname+":"+config.db_port+"/"+config.db_name)
conn = engine.connect()
Session = sessionmaker(bind=engine)
db = Session()

class db_utils:
	def __init__(self) :
		self.started = True
	def get_id(table) :
		return hex(db.query(func.count('*')).select_from(table).scalar()+1)
	def get_entity_by_name(parent, name) :
		prop = db.query(props).filter_by(ref=parent, rel="has", value=name).first()

class entities(Base) :
	__tablename__ = "entities"
	id = Column(String, primary_key=True)
	name = Column(String)

class props(Base) :
	__tablename__ = "props"
	id = Column(Integer, primary_key=True)
	ref = Column(String)
	rel = Column(String)
	value = Column(String)

	def new(name) :
		id = db_utils.get_id(props)
		p = props(ref=id, rel="name", value=type)
		db.add(p)
		db.commit()
		return id

	def set(rel, value, parent="global") :
		p = props(rel=rel, value=value, ref=parent)
		db.add(p)
		db.commit()

	def get(id) :
		res = {}
		ps = db.query(props).filter_by(ref=id).all()
		if ps != None :
			for p in ps :
				if props.__is_id(p.value) :
					res.update({p.rel : props.get(p.value)})
				else :
					res.update({p.rel : p.value})
			res.update({'ref' : id})
			return res
		return None
	def get_by_name(name) :
		return db.query(props).filter_by(rel="name", value=name).first()
	def get_by_rel(rel, value) :
		return db.query(props).filter_by(rel=rel, value=value).all()
	def __is_id(id) :
		if id[:2] == "0x" :
			return True
		return False

class states(Base) :
	__tablename__ = "states"
	id = Column(String, primary_key=True)
	state = Column(String)

	def set_or_update(key, value) :
		s = states(id=key, state=value)
		check = db.query(states).filter_by(id=key).first()
		if check == None :
			db.add(s)
		else :
			check.state = value
		db.commit()
	def get(key) :
		return db.query(states).filter_by(id=key).first()



class matrix(Base) :
	__tablename__ = "matrix"
	id = Column(String, primary_key=True)
	# weight = Column(Integer)
	parent = Column(String)
	name = Column(String)
	value = Column(String)
	# context = Column(String)

	def set(parent, name, value) :
		m = matrix(id=db_utils.get_id(matrix), parent=parent, name=name, value=value)
		db.add(m)
		db.commit()

	def get(name) :
		return db.query(matrix).filter_by(name=name).all()

class vocabulary(Base) :
	__tablename__ = "vocabulary"
	id = Column(Integer, primary_key=True)
	ref = Column(String)
	primary_value = Column(String)
	clippings = Column(String)
	past_tense = Column(String)

	def set(ref, primary, clippings, past_tense) :
		v = vocabulary(ref=ref, primary_value=primary, clippings=clippings, past_tense=past_tense)
		db.add(v)
		db.commit()
	def get(ref) :
		return db.query(vocabulary).filter_by(ref=ref).all()

if __name__ == '__main__':
	print(props.get("0x2"))



