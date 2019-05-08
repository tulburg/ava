import os, re, numpy, spacy
import tensorflow

def main() :
  average_vec("Hello world, how are you today?")


def average_vec(text) :
  nlp = spacy.load("en_core_web_md")
  tokens = nlp(text)
  print(tokens.vector)


def collect_data() :
  data = "data/bookcorpus"
  questions_file = "data/questions.txt"
  books = []
  questions = []
  nlp = spacy.load('en')
  books = [open(data+"/"+text_file, 'r').read() for text_file in os.listdir(data)]
  for book in books:
    doc = nlp(book)
    sentences = [sent.string.strip() for sent in doc.sents]
    for sentence in sentences :
      if re.compile("[?]").search(sentence) != None :
        clean = clean_text(sentence)
        print(clean)
        open(questions_file, 'a').writelines(clean)

def clean_text(text) :
  text = str(text)
  text = text.lower()

  # Clean the text
  # text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
  text = re.sub(r"what's", "what is ", text)
  text = re.sub(r"\'s", " ", text)
  text = re.sub(r"\'ve", " have ", text)
  text = re.sub(r"can't", "cannot ", text)
  text = re.sub(r"n't", " not ", text)
  text = re.sub(r"i'm", "i am ", text)
  text = re.sub(r"\'re", " are ", text)
  text = re.sub(r"\'d", " would ", text)
  text = re.sub(r"\'ll", " will ", text)
  text = re.sub(r",", " ", text)
  text = re.sub(r"\.", " ", text)
  text = re.sub(r"!", " ! ", text)
  text = re.sub(r"\/", " ", text)
  text = re.sub(r"\^", " ^ ", text)
  text = re.sub(r"\+", " + ", text)
  text = re.sub(r"\-", " - ", text)
  text = re.sub(r"\=", " = ", text)
  text = re.sub(r"'", " ", text)
  text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
  text = re.sub(r":", " : ", text)
  text = re.sub(r" e g ", " eg ", text)
  text = re.sub(r" b g ", " bg ", text)
  text = re.sub(r" u s ", " american ", text)
  text = re.sub(r"\0s", "0", text)
  text = re.sub(r" 9 11 ", "911", text)
  text = re.sub(r"e - mail", "email", text)
  text = re.sub(r"j k", "jk", text)
  text = re.sub(r"\s{2,}", " ", text)
  text = re.sub(r"\"", "", text)
  text = re.sub(r"”", "", text)
  return text

if __name__ == '__main__':
  main()