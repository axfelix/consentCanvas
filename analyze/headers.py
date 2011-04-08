
import nltk, re

# headers
# finds sections headers

def headers(txt):

    regexNumHeader = re.compile(r'[\r|\n](([A-Za-z]|[0-9]+|i+)(\.|\)))+\s+(([A-Z][a-z]+,?.)+|(\w+,?\W*)){1,8}')
    regexCapsHeader = re.compile(r'[\.|\n|\r]([A-Z]+,?\W*){1,5}')
    regexCarriageHeader = re.compile(r'[\n|\r](\w+,?[\s^\n]){1,4}[\n|\r]')
	
    numHeaderIter = regexNumHeader.finditer(txt)
    capsHeaderIter = regexCapsHeader.finditer(txt)
    regexHeaderIter = regexCarriageHeader.finditer(txt)

    numHeaderSpan = []
    for matchObj in numHeaderIter:
        numHeaderSpan.append(matchObj.span())

    capsHeaderSpan = []
    for matchObj in capsHeaderSpan:
	    capsHeaderSpan.append(matchObj.span())
		
    regexHeaderSpan = []
    for matchObj in regexHeaderSpan:
	    regexHeaderSpan.append(matchObj.span())

    headerSpan = numHeaderSpan + capsHeaderSpan + regexHeaderSpan

    return headerSpan
	
#test function
def test():
    file = open("../../eula-original-good/92.txt")
    txt = file.read()
    output = headers(txt)
    print output
    for (start, end) in output:
        print txt[start:end]

if __name__ == "__main__":
    test()