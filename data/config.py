from collections import namedtuple


config = namedtuple("config", "db_connector db_username db_password db_hostname "+
	"db_port db_name")
config.db_connector = "mysql+mysqlconnector"
config.db_username = "root"
config.db_password = "administrator"
config.db_hostname = "localhost"
config.db_port = "3307"
config.db_name = "ava"
