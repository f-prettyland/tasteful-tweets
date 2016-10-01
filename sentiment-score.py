#!/usr/bin/env python3
import nltk.classify.util
import string
import inspect
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews as train_file

def word_feats(words):
  return dict([(word, True) for word in words])

def train_model():
  negids = train_file.fileids('neg')
  posids = train_file.fileids('pos')

  negfeats = [(word_feats(train_file.words(fileids=[f])), 'neg')
              for f in negids]
  posfeats = [(word_feats(train_file.words(fileids=[f])), 'pos')
              for f in posids]

  negcutoff = int(len(negfeats)*3/4)
  poscutoff = int(len(posfeats)*3/4)

  trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
  testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
  print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

  classifier = NaiveBayesClassifier.train(trainfeats)
  print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
  return classifier
# classifier.show_most_informative_features()

def score_it(classifier, ngram):
  words = nltk.word_tokenize(ngram)
  feats = {word: True for word in words}
  print(ngram)
  print("positive", classifier.prob_classify(feats).prob('pos'))
  print("negative", classifier.prob_classify(feats).prob('neg'))


classifier = train_model()
score_it(classifier, "I like the trees")
score_it(classifier, "I hate the people")
score_it(classifier, "Crooked Hillary -- Makes History!")
