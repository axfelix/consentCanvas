
from contactInfo import contactInfo
from vlpf import vlpf
from headers import headers
from segments import segments
from preserveNewLines import preserveNewLines

# analyze
# analyzes text and returns a dictionary of found features
# @return a dictionary containing entries for
#    "vlpfs", "contactInfo", "headers", "segments"
#    each a list of (pos1, pos2) pairs of the start and end of each feature
def analyze(txt):
    positions = {}
    
    positions["contacts"] = contactInfo(txt)
    vlpfs = vlpf(txt)
    
    #top 20% (ARBITRARY) of phrases are big phrases
    #nTopVLPFs = int(0.20 * len(vlpfs))
    #positions["highVlpfs"] = vlpfs[:nTopVLPFs]
    #positions["vlpfs"] = vlpfs[nTopVLPFs:]
    try:
        positions["vlpfs"] = vlpfs
    except:
        positions["vlpfs"] = []
    
    try:
        positions["headers"] = headers(txt)
    except:
        positions["headers"] = []
    
    try:
        positions["segments"] = segments(txt)
    except:
        positions["segments"] = []
    
    try:
        positions["newlines"] = preserveNewLines(txt)
    except:
        positions["newlines"] = []
    
    return positions
    
#test function
def test():
    file = open("../../eula.txt")
    txt = file.read()
    output = analyze(txt)
    print output

if __name__ == "__main__":
    test()
