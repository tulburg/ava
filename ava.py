from lib import Mod_Spacy

spacy = Mod_Spacy()

def main() :
  spacy.update_training_data("hello world", [{"world":"(loc)", "hello":"greet"}])

if __name__ == '__main__':
  main() 