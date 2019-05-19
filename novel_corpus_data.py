import os, re, numpy, spacy
import tensorflow as tf
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, GRU


def main() :
  # collect_sent_quest_data()
  train_classifier()

def train_classifier() :
  sess = tf.Session()
  sentence_file = "data/sent_quest_type.txt"
  model_file = "data/question_classifier.ckpt"
  sentences = open(sentence_file, 'r').readlines()
  training_data_x = [s.split("|")[0].strip() for s in sentences[:87000] if len(s.split("|")) > 1 and not s.split("|")[1].strip() == '' and len(s.split("|")[1].strip()) == 1 ]
  training_data_y = [int(s.split("|")[1].strip()) for s in sentences[:87000] if len(s.split("|")) > 1 and not s.split("|")[1].strip() == '' and len(s.split("|")[1].strip()) == 1 ]
  test_data_x = [s.split("|")[0].strip() for s in sentences[87000:] if len(s.split("|")) > 1 and not s.split("|")[1].strip() == '' and len(s.split("|")[1].strip()) == 1 ]
  test_data_y = [int(s.split("|")[1].strip()) for s in sentences[87000:] if len(s.split("|")) > 1 and not s.split("|")[1].strip() == '' and len(s.split("|")[1].strip()) == 1 ] 

  tokenizer_obj = Tokenizer()
  total = test_data_x + training_data_x
  tokenizer_obj.fit_on_texts(total)

  max_length = max([len(s.split()) for s in total])
  vocab_size = len(tokenizer_obj.word_index) + 1
  training_tokens = tokenizer_obj.texts_to_sequences(training_data_x)
  test_tokens = tokenizer_obj.texts_to_sequences(test_data_x)
  training_pad = pad_sequences(training_tokens, maxlen=max_length, padding='post')
  testing_pad = pad_sequences(test_tokens, maxlen=max_length, padding='post')
  EMBEDDING_DIM = 100
  print("Building model...")
  model = Sequential()
  model.add(Embedding(vocab_size, EMBEDDING_DIM, input_length=max_length))
  model.add(GRU(units=32, dropout=0.5, recurrent_dropout=0.5))
  model.add(Dense(1, activation='sigmoid'))

  model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  print("Training model ....")
  # default epochs=25
  model.fit(training_pad, training_data_y, batch_size=128, epochs=2, validation_data=(testing_pad, test_data_y), verbose=2)

  print("Testing model....")
  tests = [
    "Hello there, how are you",
    "What is this you're talking about"
    "I'm her friend",
    "This is not what you want",
    "Can you come late today?",
    "What is that you're holding",
    "Please to meet you"
  ]
  test_tokens = tokenizer_obj.texts_to_sequences(tests)
  test_tokens_pad = pad_sequences(test_tokens, maxlen=max_length)
  print(model.predict(x=test_tokens_pad))
# def test_classifier(text) :
#   tokenizer_obj = Tokenizer()
#   test_tokens = tokenizer_obj.texts_to_sequences([text])
#   test_tokens_pad = pad_sequences(test_tokens, maxlen=70)
  print("Saving the modal....")
  saver = tf.train.Saver
  saver.save(model, model_file)



def average_vec(text) :
  nlp = spacy.load("en_core_web_md")
  tokens = nlp(text)
  print(len(tokens.vector))


def collect_data() :
  data = "data/bookcorpus"
  questions_file = "data/questions.txt"
  sentence_file = "data/sentences.txt"
  books = []
  questions = []
  nlp = spacy.load('en')
  books = [open(data+"/"+text_file, 'r').read() for text_file in os.listdir(data)]
  for book in books:
    doc = nlp(book)
    sentences = [sent.string.strip() for sent in doc.sents if not re.compile("chapter").search(sent.string.lower()) and len(sent.string) > 2]
    for index, sentence in enumerate(sentences) :
      if index < 2000 :
        if re.compile("[?]").search(sentence) != None :
          clean = clean_text(sentence)
          print("question: ", clean)
          open(questions_file, 'a').writelines(clean + "\n")
        else :
          clean = clean_text(sentence)
          print("non question: ", clean)
          open(sentence_file, 'a').writelines(clean + "\n")
      else:
        break

def collect_sent_quest_data() :
  data = "data/bookcorpus"
  sent_quest_file = "data/sent_quest_type.txt"
  nlp = spacy.load("en")
  books = [open(data+"/"+text_file, 'r').read() for text_file in os.listdir(data)]
  for book in books:
    doc = nlp(book)
    sentences = [sent.string.strip() for sent in doc.sents if not re.compile("chapter").search(sent.string.lower()) and len(sent.string) > 2]
    for index, sentence in enumerate(sentences) :
      if re.compile("[?]").search(sentence) != None :
        clean = clean_text(sentence)
        print("question: ", clean)
        open(sent_quest_file, 'a').writelines(clean + " | 1 \n")
      else :
        clean = clean_text(sentence)
        print("non question: ", clean)
        open(sent_quest_file, 'a').writelines(clean + " | 0 \n")


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
  text = re.sub(r"“", "", text)
  return text

if __name__ == '__main__':
  main()