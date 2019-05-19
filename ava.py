from lib import Mod_Spacy

spacy = Mod_Spacy()

def main() :
  # spacy.train()
  spacy.tokenize("The game is not loading");
  # spacy.update_model("my car is red in color", [{"my":"(user)", "is":"-"}])

if __name__ == '__main__':
  main() 