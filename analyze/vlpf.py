
'''
Created on Nov 16, 2010

Directly translated from: 

Kim H-rae, Chan PK. Identifying Variable-Length Meaningful Phrases with 
Correlation Functions. In: Proceedings of the 16th IEEE International
Conference on Tools with AI.; 2004:30-38.

@author: oli
'''

import sys
import string
import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

#Correlation function

def correlation_function(a, b, ab, which_fn=16):
    if which_fn == 16:
        #Piatetsky-Shapiro's
        #this should be 2nd best
        return ab - a*b
    elif which_fn == 25:
        #AEMI (Augmented Expected Mutual Information)
        #this should be the best
        raise Exception("Correlation function " + str(which_fn) + " (AEMI) is not implemented.")
    elif which_fn == 28:
        #AEMI3
        #this should be 3rd best
        raise Exception("Correlation function " + str(which_fn) + " (AEMI3) is not implemented.")
    else:
        raise Exception("Correlation function " + str(which_fn) + " is not implemented.")


def fitness_function(sim):
    #very simple as per the paper
    return (sim == 0)

#############
#Utils

def CalcPrePercentage(listOfPositions, N):
    n = len(listOfPositions)
    if (n == 0) or (N == 0):
        return 0
    
    if listOfPositions[-1] == N:
        return float(n-1) / N
    
    return float(n) / N
    

def CalcPostPercentage(listOfPositions, N):
    n = len(listOfPositions)
    if (n == 0) or (N == 0):
        return 0
    
    if listOfPositions[0] == 0:
        return float(n-1) / N
    
    return float(n) / N

def CalcIntersection(listOfPositions, N):
    if N == 0:
        return 0.0
    
    return float(len(listOfPositions)) / N



#############
# Data structure manipulation
# required because phrases (lists of strings) are unhashable

IDCounter = 0
DELIMITER = " "
#TODO: move the following variables inside functions
#      or have setup/teardown procedures
phraseAsString = {}
phraseAsID = {}


#returns a unique id
def newID():
    global IDCounter
    IDCounter += 1
    return IDCounter

# phraseAsString is a dictionary mapping the string of a phrase to an id
# phrase is a list of strings
#@return the id if it's found, -1 if not 
def getID(phrase):
    global phraseAsString
    #get string representation to index into phraseAsString
    sphrase = reduce(lambda x, y: x + DELIMITER + y, phrase)
    if not (sphrase in phraseAsString):
        id = newID()
        phraseAsString[sphrase] = id
        phraseAsID[id] = phrase 
        
    return phraseAsString[sphrase]

# converts a string representation of a phrase to a phrase (list of strings)
def string2phrase(string):
    return string.split(DELIMITER)

# converts a numerical id to a phrase (list of strings)
def id2phrase(id):
    return phraseAsID[id]

def id2string(id):
    phrase = id2phrase(id)
    sphrase = reduce(lambda x, y: x + DELIMITER + y, phrase)
    return sphrase


#############
#Main functions

GAP = -1

def BeSpecific(list, length, l, thre, seq, positionhash, corr, fitness):
    #if no l-1 length phrases stop
    if len(list[l-1]) == 0:
        return
    
    #remove nodes that are not in list[l-1] from seq
    #TODO: make this loop more efficient
    for i in range(len(seq)):
        (w, posi) = seq[i]
        if w != GAP:
            found = False
            for id in list[l-1]:
                for word in id2phrase(id):
                    if w == word:
                        found = True
                        #break
            
            if not found:
                seq[i]=(GAP, posi)
    
    #remove possible phrases that are shorter than l
    currentLength = 0
    for  i in range(len(seq)):
        (w, _) = seq[i]
        currentLength += 1
        if w == GAP:
            if currentLength < l:
                for j in range(i-currentLength, i):
                    (_, posj) = seq[j]
                    seq[j] = (GAP, posj)
            currentLength = 0
    
    #TODO: remove redundant (consecutive) GAPs for efficiency
    
    #add all l-grams from seq to list[l]
    i = -1
    n = 0
    list[l] = {}
    for (w, posi) in seq[:-l]:
        i += 1
        if w == GAP:
            continue
        else:
            lgramFound = True
            phraseToAdd = []
            for (w2, posj) in seq[i:i+l]:
                if w2 == GAP:
                    lgramFound = False
                    break
                phraseToAdd.append(w2)
            
            if lgramFound:
                n += 1
                idToAdd = getID(phraseToAdd)
                if idToAdd in positionhash:
                    positionhash[idToAdd].append( (posi, posj) )
                else:
                    positionhash[idToAdd] = [ (posi, posj) ]
                list[l][idToAdd] = -1
    length[l] = n
    
    #if l==2, calculate thre = average correlation in phrases
    avgCorr = 0.0
    n = 0.0
    
    #calculate similarities via correlation function
    for id in list[l]:
        #preprob of phrase
        addedPhrase = id2phrase(id)
        #debug
        #print addedPhrase
        A = CalcPrePercentage(positionhash[getID(addedPhrase[:l-1])], length[l-1])
        B = CalcPostPercentage(positionhash[getID([addedPhrase[-1]])], length[1])
        AB = CalcIntersection(positionhash[getID(addedPhrase)], length[l])
        list[l][id] = corr(A, B, AB)
        if l == 2:
            avgCorr += list[l][id]
            n += 1
    
    if l == 2 and n != 0:
        thre = avgCorr / n
        
    
    #Remove any phrase in list for with sim is lower then thre
    ids = list[l].keys()
    for id in ids:
        if list[l][id] < thre:
            del list[l][id]
            
    #TODO: remove phrases with posi not satisfying fitness function
    
    BeSpecific(list, length, l+1, thre, seq, positionhash, corr, fitness)


# PrunePhrases
# Removes all phrases subsumed by more meaningful (higher sim-score) superphrases
def PrunePhrases(list):
    for l in range(1, len(list)):
        ids = list[l].keys()
        for id in ids:
            current_subphrase = id2string(id)
            current_subscore = list[l][id]
            deleted=False
            for j in range(l+1, len(list)):
                for id2 in list[j]:
                    current_superscore = list[j][id2]
                    if current_superscore >= current_subscore:
                        current_superphrase = id2string(id2)
                        if string.find(current_superphrase, current_subphrase) >= 0:
                            deleted=True
                    if deleted:
                        break
                if deleted:
                    break
            if deleted:
                del list[l][id]
                

# vlpf
# looks for meaningful phrases in the text
#
# @param txt a string representing the text to be processed
#
# @return a list of (start, end) position pairs

def vlpf(txt, removeStopWords=True):
    
    #seq is a list of words in the text with positions
    #TODO: remove stop words?
    #TODO: STEM!!!
    
    #positionhash is a map from each phrase to a sorted list of position tuples of where that token 
    #begins and ends
    positionhash = {}
    
    #originalpositionhash is a map from each position in the token sequence to the character
    #position in the original unprocessed text 
    originalpositionhash = {}
    
    tokens = nltk.word_tokenize(txt)
    stopwords = nltk.corpus.stopwords.words('english')

    seq = []
    posi = 0
    origi = 0
    for token in tokens:
        tokenInStopWords = (token in stopwords)
        #add the token
        if not removeStopWords or not tokenInStopWords:
            seq.append( (token, posi) )
            if token in positionhash:
                positionhash[getID([token])].append( (posi, posi) )
            else:
                positionhash[getID([token])] = [ (posi, posi) ]
        #update the original position counter
        for c1 in token:
            while txt[origi] != c1:
                origi += 1
        #if added the token, update originalpositionhash
        if not removeStopWords or not tokenInStopWords:
            originalpositionhash[posi] = origi
            posi += 1
        
    
    # list is an array of dictionaries that store sim
    #    where   sim is a measure of similarity of the last word to the rest of the phrase
    list = {}
    list[1] = {}
    #length is the number of items in seq a a given level
    length = {}
    length[1] = len(seq)
    
    for (token, _) in seq:
        list[1][getID([token])] = 1 #sim
        
        
    #Recursive magic
    BeSpecific(list, length, 2, 0, seq, positionhash, correlation_function, fitness_function)
    
    PrunePhrases(list)
    
    phrases = []
    for k in list:
        if k == 1:
            continue
        for id in list[k]:
            sim = list[k][id]
            phrases.append( (id2phrase(id), sim) )
            
    phrases.sort(key= (lambda phrase: phrase[1]), reverse=True)
    
    #return top 15% of the phrases
    #(THIS IS CURRENTLY ARBITRARY!)
    nToReturn = int(0.15 * len(phrases))
    
    #get the start/end positions of the original text, return them
    positions = []
    for i in range(nToReturn):
        (phrase, _) = phrases[i]
        id = getID(phrase)
        for (pos1, pos2) in positionhash[id]: 
            start = originalpositionhash[pos1]
            end = originalpositionhash[pos2]
            #need to offset
            positions.append( (start + 1, end + 1) )

	#need to sort these so I can pull out top top several for warning/quote div		
    return positions


#################
# test function #
#################



def test():
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        #local test
        #in final version we may want to print out use information here
        filenames = ["../../eula.txt"] 
    
    #run algorithm for each filename
    for filename in filenames:
        #TODO: insert try/except
        file = open(filename)
        txt = file.read()
        positions = vlpf(txt)
        
        for pos in positions:
            print pos
        for (start, end) in positions:
            print txt[start:end]
            
#main entry point to the program
if __name__ == '__main__':
    test()
