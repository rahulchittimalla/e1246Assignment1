import nltk
import re
import numpy as np
from nltk.corpus import brown

import time




def myNGrams(text, grams):
    model = []

    tokens = list(text.split())
    i = 1
    while i <= grams:
        count = 0
        for token in tokens[:len(tokens)-i+1]:
            model.append(tuple(tokens[count:count+i]))
            count = count+1
        i = i+1
    return model

def getFreq(n):
    freq = {}
    length = {}

    for category in brown.categories():
        sentences = brown.sents(categories = category)
        length[category] =  len(sentences)
        for sentence in sentences[:int(length[category]*0.9)]:
            text = " <s> " + ' '.join(re.compile(r'\w+').findall(' '.join(sentence))).lower() +" </s> "
            model = myNGrams(text, n)
            for x in model:
                line = ' '.join(x)
                count = len(re.findall(" "+line+" ", text))
                if (x not in freq) and (count <> 0):
                    freq[x] = 0
                if count <> 0:
                    freq[x] += count
    return [freq, length]

def perplexity(freq, length, n):
    prob = 0.0
    N = 0
    print length
    for key in length:
        sentences = brown.sents(categories = key)
        for sentence in sentences[int(length[key] * 0.95):int(length[key]*0.95 + length[key]*0.05)]: #length[key]:int(length[key] + length[key]*0.1)
            text = "<s> " + ' '.join(re.compile(r'[a-zA-Z]+').findall(' '.join(sentence))).lower() +" </s>"
            N += len(text.split()) - 1
            model = ngrams(text, n)
            for x in model:
                p = probability(x, freq, n)
                if p > 0:
                    prob += np.log2(p)
    prob = -prob/float(N)
    pp = 2**(prob)
    return pp


def probability(x, freq, n):
    if x in freq:
        prob = freq[x]/float(freq[x[:n-1]])
    else:
        i = 1
        while i < n:
            if i == n-1:
                count = 0
                for key in freq:
                    if len(key) == 1:
                        count += freq[key]
                if x[i:] in freq:
                    prob = freq[x[i:]]/float(count)
                else:
                    prob = 1/float(count)

            else:
                if x[i:] in freq:
                    prob = freq[x[i:]]/float(freq[x[i:n-1]])
                    break
            i = i+1
    return prob

def ngrams(text, grams):
    model = []
    count = 0
    tokens = list(text.split())
    for token in tokens[:len(tokens)-grams+1]:
        model.append(tuple(tokens[count:count+grams]))
        count = count+1
    return model

def main():
    n = 4
    freq, length = getFreq(n)
    print "it returned"
    pp = perplexity(freq, length, n)
    print("perplexity for n= {0}").format(n)
    print pp

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
