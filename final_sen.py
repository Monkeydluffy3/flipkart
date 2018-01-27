import nltk 
import random 
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

class voteClassifier(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers = classifiers
        
    def classify(self,features):
        votes = []
        for c in self._classifiers:
           v = c.classify(features)
           votes.append(v)
        return mode(votes)
    
    def confindence(self,features):
        votes = []
        for c in self._classifiers:
           v = c.classify(features)
           votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf         


documents_f = open("documents.pickle","rb")
documents = pickle.load(documents_f)
documents_f.close()
      
           

word_features_f = open("word_features.pickle","rb")
word_features = pickle.load(word_features_f)
word_features_f.close()

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
        
    return features


featuresets_f = open("featuresets.pickle","rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()


training_set = featuresets[:4000]
testing_set = featuresets[4000:]

open_file = open("original.pickle","rb")
classifier = pickle.load(open_file)
open_file.close()
print("accuracy : ",(nltk.classify.accuracy(classifier,testing_set))*100)


open_file = open("MNB_classifier.pickle","rb")
MNB_classifier = pickle.load(open_file)
open_file.close()
print("accuracy : ",(nltk.classify.accuracy(MNB_classifier,testing_set))*100)

open_file = open("BernoulliNB.pickle","rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()
print("accuracy : ",(nltk.classify.accuracy(BernoulliNB_classifier,testing_set))*100)

voted_classifier = voteClassifier(classifier,BernoulliNB_classifier,MNB_classifier)


def sentiment(text):
    feats = find_features(text)
    
    return voted_classifier.classify(feats),voted_classifier.confindence(feats)
