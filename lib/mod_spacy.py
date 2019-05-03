import ast
import random
import spacy
from spacy.util import minibatch, compounding

from core.module import Module, Util
log = Util.log
config = {
  "name": "Spacy Module",
  "version": "0.0.1",
  "dependencies": {}
}

class Mod_Spacy(Module) :

  def __init__(self) :
    self.config = config
    super(Mod_Spacy, self).__init__()

  def update_training_data(self, text, tokens) :
    data = text + ":" + "["
    for token in tokens :
      for key, value in token.items() :
        start = data.index(key)
        end = start + len(key)
        data += f"({start}, {end}, \"{value}\"),"
      data += "]"
    # with open("data/spacy_token_training_data", "a") as f:
    #   f.write(f"{data}\n")
  
  def train(self) :
    pass