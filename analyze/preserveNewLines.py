


def preserveNewLines(txt):
    
    positions = []
    for i in range(len(txt)):
        if txt[i] == '\n':
            positions.append(i)
    
    return positions


            
