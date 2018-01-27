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

short_pos = open("positive.txt","r",encoding='utf-8', errors='replace').read()
short_neg = open("negative.txt","r",encoding='utf-8', errors='replace').read()

documents =[]
all_words=[]

allowed_word_types = ["J"]

for p in short_pos.split('\n'):
    documents.append((p,'pos'))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
         if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
            
for p in short_neg.split('\n'):
    documents.append((p,'neg'))
    words = word_tokenize(p)
    neg = nltk.pos_tag(words)
    for w in neg:
         if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

save_documents = open("documents.pickle","wb")
pickle.dump(documents,save_documents)
save_documents.close()
      
            
all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:2000]

save_word_features = open("word_features.pickle","wb")
pickle.dump(word_features,save_word_features)
save_word_features.close()

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
        
    return features      

featuresets=[(find_features(rev),category) for (rev,category) in documents]
random.shuffle(featuresets)  

save_featuresets = open("featuresets.pickle","wb")
pickle.dump(featuresets,save_featuresets)
save_featuresets.close()

training_set = featuresets[:4000]
testing_set = featuresets[4000:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("accuracy : ",(nltk.classify.accuracy(classifier,testing_set))*100)

save_classifier = open("original.pickle","wb")
pickle.dump(classifier,save_classifier)
save_classifier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB accuracy : ",(nltk.classify.accuracy(MNB_classifier,testing_set))*100)

save_MNB_classifier = open("MNB_classifier.pickle","wb")
pickle.dump(MNB_classifier,save_MNB_classifier)
save_MNB_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB accuracy : ",(nltk.classify.accuracy(BernoulliNB_classifier,testing_set))*100)

save_BernoulliNB_classifier = open("BernoulliNB.pickle","wb")
pickle.dump(BernoulliNB_classifier,save_BernoulliNB_classifier)
save_BernoulliNB_classifier.close()

voted_classifier = voteClassifier(classifier)

#print("voted : ",(nltk.classify.accuracy(voted_classifier,testing_set))*100)
#classifier.show_most_informative_features(15)

def sentiment(text):
    feats = find_features(text)
    
    return voted_classifier.classify(feats)
