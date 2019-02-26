from preprocess import *
import pickle
import os

def lm_train(data_dir, language, fn_LM):
    """
	This function reads data from data_dir, computes unigram and bigram counts,
	and writes the result to fn_LM
	
	INPUTS:
	
    data_dir	: (string) The top-level directory continaing the data from which
					to train or decode. e.g., '/u/cs401/A2_SMT/data/Toy/'
	language	: (string) either 'e' (English) or 'f' (French)
	fn_LM		: (string) the location to save the language model once trained
    
    OUTPUT
	
	LM			: (dictionary) a specialized language model
	
	The file fn_LM must contain the data structured called "LM", which is a dictionary
	having two fields: 'uni' and 'bi', each of which holds sub-structures which 
	incorporate unigram or bigram counts
	
	e.g., LM['uni']['word'] = 5 		# The word 'word' appears 5 times
		  LM['bi']['word']['bird'] = 2 	# The bigram 'word bird' appears 2 times.
    """
	
	# TODO: Implement Function
    files = os.listdir(data_dir) # all file names
    LM = {'uni':{}, 'bi':{}}
    for file in files:
        if file[-1] == language:
            with open(os.path.join(data_dir, file), 'r') as f:
                sentences = f.readlines()
                for sentence in sentences:
                    temp = preprocess(sentence, language).split(" ")
                    for i in range(0, len(temp)-1): # calculate uni-gram
                        item = temp[i]
                        if item in LM['uni']:
                            LM['uni'][item] += 1
                        else:
                            LM['uni'][item] = 1
                    for i in range(0, len(temp) - 1):# calculate bi-gram
                          w1 = temp[i]
                          w2 = temp[i+1]
                          if w1 in LM['bi']:
                              if w2 in LM['bi'][w1]:
                                  LM['bi'][w1][w2] += 1
                              else:
                                  LM['bi'][w1][w2] = 1
                          else:
                              LM['bi'][w1] = {w2:1}
    language_model = LM
    #Save Model
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    return language_model