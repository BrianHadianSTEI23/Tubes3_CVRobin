

# specification: get the bad match table, then do pattern matching from the end

def getBadMatchTable(pattern : str) -> dict[str, int]:

    '''algorithm
    1. get all different types of letters in the patter
    2. put into bad match table
    3. run through the pattern for its index'''

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    badMatchTable : dict[str, int]= {}
    # fill bad match table with all alphabet
    for i in range(len(alphabet)):
        badMatchTable.update({alphabet[i].lower() : -1})

    for j in range(len(pattern)) :
        badMatchTable.update({ pattern[j] : j})

    return badMatchTable

def boyerMooreMatch(text : str, keywords : list[str]) -> dict[str, int]:

    result = {}

    for keyword in keywords:
        if len(text) >= len(keyword) :
            iterForText = len(keyword) - 1
            iterForPattern = len(keyword) - 1 
            # determine its bad match table
            badMatchTable = getBadMatchTable(keyword)
            while (iterForText < (len(text) - len(keyword))):

                if (text[iterForText] == keyword[iterForPattern] and (iterForPattern == 0)):
                    if (keyword in result.keys()):
                        result.update({keyword : result[keyword] + 1})
                    else : # hasn't been there
                        result.update({ keyword : 1})
                    iterForPattern = len(keyword) - 1 
                    iterForText += len(keyword)
                elif (text[iterForText] == keyword[iterForPattern]):
                    iterForText -= 1
                    iterForPattern -= 1
                else : # not the same
                    if (badMatchTable[text[iterForText]] > -1): 
                        if (badMatchTable[text[iterForText]] < iterForPattern): # occurs again later
                            iterForText += max(1, iterForPattern - badMatchTable[text[iterForText]])
                        else : # not occurs again later
                            iterForText += len(keyword) - iterForPattern
                    else : # not in bad match table
                        iterForText += len(keyword)
                    iterForPattern = len(keyword) - 1 # go back to the last

    return result
