

# algorithm : get the longest 

def getBorderTable(pattern : str) -> dict[int, int] : # list of char

    borderTable = {}
    startIndex = 0
    borderTable.update({startIndex : startIndex}) # initialization

    iterForPrefix = 0 
    iterForSuffix = 1
    while (iterForSuffix < len(pattern)):
        if (pattern[iterForSuffix] == pattern[iterForPrefix]):
            borderTable.update({ iterForSuffix : iterForPrefix + 1})
            iterForPrefix += 1
            iterForSuffix += 1
        elif (iterForPrefix > 0):
            iterForPrefix = borderTable[iterForPrefix - 1]
        else :
            borderTable.update({ iterForSuffix : 0}) # this is for handling when the first character is already not the same, then just assign 0 to the table (for that index) and then move forward in the pattern
            iterForSuffix += 1
    return borderTable

def knuthMorrisPrattMatch(text : str, keywords : list[str]) -> dict[str, int]:

    result = {}

    for keyword in keywords:
        iterForSuffix = 0 
        iterForPrefix = 0 
        # determine its border table
        borderTable = getBorderTable(keyword)
        while (iterForSuffix < len(text)):

            if (text[iterForSuffix] == keyword[iterForPrefix] and (iterForPrefix == len(keyword) - 1)):
                if (keyword in result.keys()):
                    result.update({keyword : result[keyword] + 1})
                else : # hasn't been there
                    result.update({ keyword : 1})
                iterForPrefix = 0
            elif (text[iterForSuffix] == keyword[iterForPrefix]):
                iterForPrefix += 1
                iterForSuffix += 1
            elif (iterForPrefix > 0) : # if not the same
                iterForPrefix = borderTable[iterForPrefix - 1]
            else : # iter for prefix = 0
                iterForSuffix += 1
 
    return result

# debug
if __name__ == "__main__":
    print(knuthMorrisPrattMatch("hayo apa hayo", ["ao"]))