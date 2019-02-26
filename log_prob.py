from preprocess import *
from lm_train import *
from math import log

def log_prob(sentence, LM, smoothing=False, delta=0, vocabSize=0):
    """
	Compute the LOG probability of a sentence, given a language model and whether or not to
	apply add-delta smoothing
	
	INPUTS:
	sentence :	(string) The PROCESSED sentence whose probability we wish to compute
	LM :		(dictionary) The LM structure (not the filename)
	smoothing : (boolean) True for add-delta smoothing, False for no smoothing
	delta : 	(float) smoothing parameter where 0<delta<=1
	vocabSize :	(int) the number of words in the vocabulary
	
	OUTPUT:
	log_prob :	(float) log probability of sentence
	"""
	
	#TODO: Implement by student.
    V = len(LM['uni'])
    log_prob = 0
    sentence = sentence.split(" ")
    for i in range(len(sentence)-1):
        w1 = sentence[i]
        w2 = sentence[i+1]
        if w1 not in LM['uni'] or w1 not in LM['bi'] or w2 not in LM['bi'][w1]:
            prob = float('-inf')
        else:
            prob = log2(LM['bi'][w1][w2] + delta) - log2((LM['uni'][w1] + delta*V))
        log_prob += prob
    return log_prob