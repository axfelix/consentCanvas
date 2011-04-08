
import nltk, re

# contactInfo
# finds URLs, phone numbers, email addresses and bolds them

def contactInfo(txt):

    regexPhone = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})')
    regexEmail = re.compile(r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}\b')
    regexUrl = re.compile(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')

    phoneIter = regexPhone.finditer(txt)
    emailIter = regexEmail.finditer(txt)
    urlIter = regexUrl.finditer(txt)
    
    phoneSpan = []
    for matchObj in phoneIter:
        phoneSpan.append(matchObj.span())
        
        
    emailSpan = []
    for matchObj in emailIter:
        emailSpan.append(matchObj.span())
    
    urlSpan = []
    for matchObj in urlIter:
        urlSpan.append(matchObj.span())
    
    allSpans = phoneSpan + emailSpan + urlSpan
    
    return allSpans
	
#test function
def test():
    file = open("../../eula-original-good/92.txt")
    txt = file.read()
    output = contactInfo(txt)
    print output
    for (start, end) in output:
        print txt[start:end]

if __name__ == "__main__":
    test()