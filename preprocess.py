import re

def preprocess(in_sentence, language):
    """ 
    This function preprocesses the input text according to language-specific rules.
    Specifically, we separate contractions according to the source language, convert
    all tokens to lower-case, and separate end-of-sentence punctuation 
	
	INPUTS:
	in_sentence : (string) the original sentence to be processed
	language	: (string) either 'e' (English) or 'f' (French)
				   Language of in_sentence
				   
	OUTPUT:
	out_sentence: (string) the modified sentence
    """
    sentence = in_sentence.lower()
    sentence = sentence.rstrip("\n ")# remove newline sign and space at the tail
    operator = r"\s*[=\+\-\*\/><\^%]+\s*" # math operator
    punctuation = r"\s*[-?!.,:;\(\)\[\]\{\}\'\"]+\s*"# punctuation
    pattern = "("+ operator + "|" + punctuation + ")"
    apostrophe = r"([a-z]+\'[a-z]+|[a-z]+[s]\')" # apostrophe for english words
    sentence = re.split(apostrophe, sentence)
    for i in range(len(sentence)):
      if i%2 == 0: # only manipulate non-apostrophes
        listing = re.split(pattern, sentence[i])
        for j in range(len(listing)):
            if j%2 == 1:
              item = listing[j].strip(" ")
              item = " ".join([k for k in item if k !=" "])
              listing[j] = item.strip(" ")
        listing = [item for item in listing if item != ""]
        sentence[i] = " ".join(listing)
    sentence = [item.strip(" ") for item in sentence if item != ""]
    sentence = " ".join(sentence)
    if language is "f":
      qu = r"(?<=\b)\s*qu\'(?=\w)"
      consonant = r"(?<=\b)\s*\w*[bcfghjklmnpqrstvwxz]\'(?=\w)"
      il = r"(?<=\w\')il\W*(?=\w|$)"
      on = r"(?<=\w\')on\W*(?=\w|$)"
      pattern = "(" + qu + "|" + il + "|" + on  + "|" + consonant + ")" 
      sentence = re.split(pattern, sentence, flags=re.IGNORECASE)
      for i in range(len(sentence)):
        item = sentence[i].strip(" ")
        if i%2 == 1 and "\'" in item:
          item = "\'".join([i for i in re.split(r"\s*\'\s*", item)])
          sentence[i] = item
      sentence = [item for item in sentence if item != ""]
      sentence = " ".join(sentence)
      items = re.findall(r'(?<=\b)d\'\w+\b', sentence, flags=re.IGNORECASE)
      for item in items:
        if item not in [r"d'abord", r"d'accord", r"d'ailleurs", r"d'habitude"]:
          temp = re.split(r"(\w\')", item)
          temp = [ele for ele in temp if ele !="" and ele != None]
          sentence = sentence.replace(item, " ".join(temp))
    out_sentence = 'SENTSTART ' + sentence.strip(" ") + ' SENTEND'
    return out_sentence