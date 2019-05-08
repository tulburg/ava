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

  def update_model(self, text, tokens) :
    data = text + ":" + "["
    for token in tokens :
      for key, value in token.items() :
        start = data.index(key)
        end = start + len(key)
        data += f"({start}, {end}, \"{value}\"),"
      data += "]"
    with open("data/spacy_token_training_data", "a") as f:
      f.write(f"{data}\n")
    # retrain the model
    self.train()

  def train(self) :
    # load training data from file
    TRAINING_DATA = []
    training_sets = []
    with open("data/spacy_token_training_data", "r") as f :
      training_sets = f.readlines()
    for training_set in training_sets :
      set = training_set.split(":")
      TRAINING_DATA.append((set[0], {"entities": ast.literal_eval(set[1])}))
    
    # load model 
    nlp = spacy.load("data/spacy_token_model")
    if "ner" not in nlp.pipe_names:
      ner = nlp.create_pipe("ner")
      nlp.add_pipe(ner, last=True)
    else:
      ner = nlp.get_pipe("ner")
    for _, annotations in TRAINING_DATA:
      for ent in annotations.get("entities"):
        ner.add_label(ent[2])

    # train pipe
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes): 
      nlp.begin_training()
      for itn in range(10000):
        random.shuffle(TRAINING_DATA)
        losses = {}
        batches = minibatch(TRAINING_DATA, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
          texts, annotations = zip(*batch)
          nlp.update(texts, annotations, drop=0.5, losses=losses)
        log("Losses %s", (losses))

    # save back to disk
    nlp.to_disk("data/spacy_token_model")

  def tokenize(self, text) :
    nlp = spacy.load("data/spacy_token_model")
    doc = nlp(text)
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
    print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # return (text, tokenized_text)