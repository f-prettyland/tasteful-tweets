#!/usr/bin/env python3
import nltk.classify.util
import string
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews as train_file
from parser_of_words import loadWords, loadDictionary

classes = ['neg', 'pos']
class_mod = [-100, 70]
terrible_adjustment = -50
terrible_nouns = []

def word_feats(words):
  return dict([(word, True) for word in words])

def train_model_and_prepare():
  global terrible_nouns
  terrible_nouns = loadWords('dict/terrible.txt')
  return train_model()

def train_model():
  negids = train_file.fileids(classes[0])
  posids = train_file.fileids(classes[1])

  negfeats = [(word_feats(train_file.words(fileids=[f])), classes[0])
              for f in negids]
  posfeats = [(word_feats(train_file.words(fileids=[f])), classes[1])
              for f in posids]

  negcutoff = int(len(negfeats)*3/4)
  poscutoff = int(len(posfeats)*3/4)

  trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
  testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
  print('train on %d instances, test on %d instances' % (len(trainfeats),
        len(testfeats)))

  classifier = NaiveBayesClassifier.train(trainfeats)
  print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
  return classifier
# classifier.show_most_informative_features()

def score_it(classifier, ngram):
  if classifier:
    words = nltk.word_tokenize(ngram)
    feats = {word: True for word in words}
    num_terrible = sum(map(lambda x: x in terrible_nouns if 1 else 0, ngram))
    score = num_terrible * terrible_adjustment
    for c in range(len(classes)):
      class_prob = classifier.prob_classify(feats).prob(classes[c])
      # print(classes[c], class_prob) # for debug
      score += class_mod[c] * class_prob
    return score
  else:
    raise Exception('Have not trained model')

# classifier = train_model()
# score_it(classifier, "I like the trees")
# score_it(classifier, "I hate the people")
# score_it(classifier, "Crooked Hillary -- Makes History!")
