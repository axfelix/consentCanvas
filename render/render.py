
import markup

# render
# applies CSS properties to texted selected by other submodules
# outputs a valid HTML5 document



def render(txt, contacts=[], vlpfs=[], headerSpan=[], highVlpfs=[], tiles=[], newlines = []):
# inserting tags into text
# (hopefully) traverses list of positions backwards so that
#	we don't need to count how many chars are being inserted

    if len(tiles) > 2:
        leadTiles = tiles[:1]
    else:
        leadTiles = tiles
    
    masterList = []
    strongList = contacts + vlpfs
    if vlpfs:
        bestVlpf = vlpfs[0]
        #bestVlpf = highVlpfs[0]
    else:
        bestVlpf = None
    for (start, end) in strongList:
        masterList.append( ('</strong>',end) )
        masterList.append( ('<strong>',start) )
	
    for (start, end) in headerSpan:
	    masterList.append( ('</h2><p>',end ))
	    masterList.append( ('</p><h2>',start) )
	
    for (start, end) in highVlpfs:
	    masterList.append( ('</p></div><p>',end) )
	    masterList.append( ('</p><div class=\"warning\"><p>',start) )
		
    for (start, end) in leadTiles:
	    masterList.append( ('</p><p>',end) )
	    masterList.append( ('</p><p class=\"lead\">',start) )
    
    for pos in newlines:
        masterList.append( ("<br>", pos) )
		
# sort by position, may need to reverse
    masterList.sort(key = lambda item: item[1], reverse=True)

    (pullStart, pullEnd) = bestVlpf
    pullQuote = txt[pullStart:pullEnd]
# need to actually clarify what tag and pos are pointing at...
    for (tag, pos) in masterList:
	    txt = txt[:pos] + tag + txt[pos:]

    page = markup.page( )
    page.init(	title='Consent Canvas Document',
			css='textured-agreement-clean-1.css')
    page.h1('Consent Canvas Document')
    page.body(class_='textured-agreement hyphenate')
    page.div(class_="aside")
    
    # insert #1 vlpf -- yes, the stylesheet uses 2 divs here.

    if bestVlpf:
        page.div(class_='quote donthyphenate')
        page.div(pullQuote)
        page.div.close()
        page.div.close()
    page.div.close()
    page.p(txt)
    page.body.close()
    #print page
    #texturedEula.write(str(page))
    return page
	
	

#test function
def test():
    file = open("../../eula.txt")
    txt = file.read()
    output = render(txt, allSpans, positions, headerSpan, highVlpfs, leadTile)
    texturedEula = open('textured.html','w')

if __name__ == "__main__":
    test()