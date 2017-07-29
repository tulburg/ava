CREATE TABLE IF NOT EXISTS memory (
	id varchar(100) not null primary key, 
	weight int(11) not null,
	parent text not null,
	name text not null,
	value text not null
);

CREATE TABLE IF NOT EXISTS props (
	id int(11) not null auto_increment primary key,
	ref varchar(100) not null,
	rel text not null,
	value text not null
);

CREATE TABLE IF NOT EXISTS entities (
	id varchar(100) not null primary key,
	name text not null
);

CREATE TABLE IF NOT EXISTS vocabulary (
	id int(11) not null auto_increment primary key,
	ref text not null,
	primary_value text not null,
	clippings text not null,
	past_tense text not null
);

CREATE TABLE IF NOT EXISTS matrix (
	id varchar(100) not null primary key,
	weight int(11) not null,
	parent text not null,
	name text not null,
	value text not null,
	context text not null
);

CREATE TABLE IF NOT EXISTS states (
	id varchar(100) not null primary key,
	state text not null
);