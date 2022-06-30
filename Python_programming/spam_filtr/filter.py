import basefilter
import trainingcorpus

from collections import Counter
from itertools import chain
from math import log10

class MyFilter(basefilter.BaseFilter):
    def give_counted_dict(self,TAG):
        tokens = []
        for filename,filebody in self.tc.spam_ham_generator(TAG):
            tokens.append(self.tc.get_tokens(filebody))
        tokens = list(chain(*tokens))

        return tokens, dict(Counter(tokens))
    def give_probability(self,counted,tokens):
        
        count_uniq = len(counted) * self.sigma
        probability = dict()
        for key in counted.keys():
            value = counted[key]
            probability[key] = log10( (value + self.sigma)/(len(tokens) + count_uniq) ) 
        
        return probability
    
    def merge_dictionaries(self,counted_spam, counted_ham):
        for key in counted_spam.keys():
            counted_spam[key]+=self.sigma
        for key in counted_ham.keys():
            counted_ham[key]+=self.sigma
            if key not in counted_spam:
                counted_spam[key] = self.sigma
        
        for key in counted_spam.keys():
            if key not in counted_ham:
                counted_ham[key] = self.sigma
            
            

    def train(self,path):
        self.tc = trainingcorpus.TrainingCorpus(path)
        tokens_spam, counted_spam = self.give_counted_dict(self.tc.SPAM_TAG)
        tokens_ham, counted_ham = self.give_counted_dict(self.tc.HAM_TAG)
        self.sigma =  1.625 #pro slova, ktera nejsou v jinem dictu
        
        self.merge_dictionaries(counted_spam,counted_ham)

        self.spamwords_probability = self.give_probability(counted_spam,tokens_spam)
        self.hamwords_probability = self.give_probability(counted_ham,tokens_ham)

        self.spam_probability = log10(self.tc.spam_count / (self.tc.spam_count + self.tc.ham_count))
        self.ham_probability = log10(self.tc.ham_count / (self.tc.spam_count + self.tc.ham_count))
    
    def make_decision(self,filebody):
        tokens = self.tc.get_tokens(filebody)
        counted = dict(Counter(tokens))
        spam_p = self.spam_probability
        ham_p = self.ham_probability
        for word in tokens:
            if word in self.tc.ignore_list:
                continue
            if word not in self.spamwords_probability and word not in self.hamwords_probability:
                continue

            spam_p+= self.spamwords_probability[word]
            ham_p+= self.hamwords_probability[word]
            
        if(spam_p > ham_p):
            return self.tc.SPAM_TAG
        if(spam_p < ham_p):
            return self.tc.HAM_TAG

    def test(self, path):
        super().make_corpus(path)

        for filename, filebody in self.corp.emails():

            super().write_decision(filename,self.make_decision(filebody))
        super().close_file()