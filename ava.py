import multiprocessing, sys, signal
from manager import Manager
from mind import Mind
from modules.environment import Environment
from modules.relationship import Relationship
from generator import Generator


queue = multiprocessing.Queue()
fn = sys.stdin.fileno()
manager = Manager(queue)
generator = Generator()

environment = Environment(manager, generator)
relationship = Relationship(manager, generator)

# manager = multiprocessing.Process(target=manager)
mind = multiprocessing.Process(target=Mind, args=(manager,fn))

mind.start()
manager.start()

def signal_handler(signal, frame) :
	manager.unpack()
	environment.unpack()
	relationship.unpack()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.pause()

