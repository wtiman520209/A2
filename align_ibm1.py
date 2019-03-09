from lm_train import *
from log_prob import *
from preprocess import *
from math import log
import os

def align_ibm1(train_dir, num_sentences, max_iter, fn_AM):
    """
	Implements the training of IBM-1 word alignment algoirthm. 
	We assume that we are implemented P(foreign|english)
	
	INPUTS:
	train_dir : 	(string) The top-level directory name containing data
					e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
	num_sentences : (int) the maximum number of training sentences to consider
	max_iter : 		(int) the maximum number of iterations of the EM algorithm
	fn_AM : 		(string) the location to save the alignment model
	
	OUTPUT:
	AM :			(dictionary) alignment model structure
	
	The dictionary AM is a dictionary of dictionaries where AM['english_word']['foreign_word'] 
	is the computed expectation that the foreign_word is produced by english_word.
	
			LM['house']['maison'] = 0.5
	"""
    AM = {}
    
    # Read training data
    (eng, fre) = read_hansard(train_dir, num_sentences)
    
    # Initialize AM uniformly
    AM = initialize(eng, fre)
    
    # Iterate between E and M steps
    for i in range(max_iter):
      em_step(AM, eng, fre)
    with open(fn_AM+'.pickle', 'wb') as handle:
        pickle.dump(AM, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return AM
#    return language_model

    return AM
    
# ------------ Support functions --------------
def read_hansard(train_dir, num_sentences):
    """
	Read up to num_sentences from train_dir.
	
	INPUTS:
	train_dir : 	(string) The top-level directory name containing data
					e.g., '/u/cs401/A2_SMT/data/Hansard/Testing/'
	num_sentences : (int) the maximum number of training sentences to consider
	
	
	Make sure to preprocess!
	Remember that the i^th line in fubar.e corresponds to the i^th line in fubar.f.
	
	Make sure to read the files in an aligned manner.
	"""
    # TODO
    eng = []
    fre = []
    num_eng = 0
    num_fre = 0
    files = os.listdir(data_dir) # all file names
    for file in files:
      with open(os.path.join(data_dir, file), 'r') as f:
        sentences = f.readlines()
      n = len(sentences)
      if file[-1] == 'e' and num_eng < num_sentences:
        if num_eng + n <= num_sentences:
          eng.extend(sentences)
        else:
          eng.extend(sentence[0:num_sentences - num_fre])
        num_eng = len(eng)
      else:
        if num_fre + n <= num_sentences:
          fre.extend(sentences)
        else:
          fre.extend(sentence[0:num_sentences - num_fre])
        num_fre = len(fre)
      if num_eng == num_fre and num_eng == num_sentences:
        break
    return (eng, fre)

def initialize(eng, fre):
    """
	Initialize alignment model uniformly.
	Only set non-zero probabilities where word pairs appear in corresponding sentences.
	"""
	# TODO
    t = {}
    t["SENTSTART"] = {"SENTSTART":1}
    t["SENTEND"] = {"SENTEND":1}
    num_sentences = len(eng)
    for i in range(num_sentences):
      list_eng = eng[i].split(" ")
      list_fre = fre[i].split(" ")
      for word_eng in list_eng:
        if word_eng == 'SENTSTART' or word_eng == 'SENTEND':
          continue
        if word_eng not in t:
          t[word_eng] = {}
        for word_fre in list_fre:
          if word_fre in t[word_eng]:
            t[word_eng][word_fre] += 1
          else:
            t[word_eng][word_fre] = 1
    for word_eng  in t:
      num = 0
      for word_fre in t[word_eng]:
        num += t[word_eng][word_fre]
      for word_fre in t[word_eng]:
        t[word_eng][word_fre] /= num
    return t

def em_step(t, eng, fre):
    """
	One step in the EM algorithm.
	Follows the pseudo-code given in the tutorial slides.
	"""
	# TODO
    tcount = {}
    total = {}
    for word_eng in t:
      total[word_eng] = 0
      for word_fre in t[word_eng]:
        t[word_eng][word_fre] = 0
    num_sentences = len(eng)
    for i in range(num_sentences):
      list_eng = eng[i].split(" ")
      list_fre = fre[i].split(" ")
      for word_fre in set(list_fre):
        denom_c = 0
        for word_eng in set(list_eng):
          denom_c += t[word_eng][word_fre]*list_fre.count(word_fre)
        for word_eng in set(list_eng):
          tcount[word_eng][word_fre] += t[word_eng][word_fre]*list_fre.count(word_fre)*list_eng(word_eng)/denom_c
          total[word_eng] = t[word_eng][word_fre]*list_fre.count(word_fre)*list_eng(word_eng)/denom_c
    for word_eng in total:
      for word_fre in tcound[word_eng]:
        t[word_eng][word_fre] = tcound[word_eng][word_fre]/total[word_eng]