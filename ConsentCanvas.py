import sys
from analyze.analyze import analyze
from render.render import render

def PrintUsage():
    print "Usage: ConsentCanvas.py <eula1>"


def texturize(txt):
    analyzeDictionary = analyze(txt)
    output = render(txt
                    ,contacts = analyzeDictionary["contacts"]
                    ,vlpfs = analyzeDictionary["vlpfs"]
                    ,headerSpan = analyzeDictionary["headers"]
                    #,highVlpfs = analyzeDictionary["highVlpfs"]
                    #,leadTile = ...
                    ,newlines = analyzeDictionary["newlines"]
                    ,tiles = analyzeDictionary["segments"]
                    )
    return output

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        PrintUsage()
    else:
        filename = sys.argv[1]
        file = open(filename)
        txt = file.read()
        
        print texturize(txt)
        texturedEula = open((filename + '-canvas.html'),'w')
        texturedEula.write(str(texturize(txt))) 