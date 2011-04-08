
import nltk
from nltk.tokenize.texttiling import TextTilingTokenizer


# segments
# finds locations to split txt into cohesive sections
# @return a list of (start, end) pairs for each section, although the end of each
#         section should be the start of the next
#
# for now
def segments(txt):
    
    ttt = TextTilingTokenizer()
    tokens = ttt.tokenize(txt)
    
    start = 0
    end = 0
    tileSpan = []
    
    for token in tokens:
        end = start + len(token)
        tileSpan.append((start, end))
        start = end
    return tileSpan



#test function
def test():
    file = open("../../eula.txt")
    txt = file.read()
    output = segments(txt)
    print output

if __name__ == "__main__":
    test()