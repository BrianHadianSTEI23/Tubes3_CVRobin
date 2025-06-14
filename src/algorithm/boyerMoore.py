import re

# specification: get the bad match table, then do pattern matching from the end

def clean_alnum_only(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9 ]', '', s.lower())


def getBadMatchTable(pattern : str) -> dict[str, int]:

    '''algorithm
    1. get all different types of letters in the patter
    2. put into bad match table
    3. run through the pattern for its index'''

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", "a", "b",
                "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ":", "/", "\\", "'", "\"", "?",
                ">", "<", "]", "[", "{", "}", "|", "!", "@", "#"," $", "%", "^", "&", "*", "(", ")", "+", "_", "-", "=", "`", "~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                "\n", ",", "."]
    badMatchTable : dict[str, int]= {}
    # fill bad match table with all alphabet
    for i in range(len(alphabet)):
        badMatchTable.update({alphabet[i] : -1})

    for j in range(len(pattern)) :
        badMatchTable.update({ pattern[j] : j})

    return badMatchTable

def boyerMooreMatch(text : str, keywords : list[str]) -> dict[str, int]:

    result = {}
    clean_text = clean_alnum_only(text)

    for keyword in keywords:
        if len(text) >= len(keyword) :
            iterForText = len(keyword) - 1
            iterForPattern = len(keyword) - 1 
            # determine its bad match table
            badMatchTable = getBadMatchTable(keyword)
            while (iterForText < len(clean_text)):

                if (clean_text[iterForText] == keyword[iterForPattern] and (iterForPattern == 0)):
                    if (keyword in result.keys()):
                        result.update({keyword : result[keyword] + 1})
                    else : # hasn't been there
                        result.update({ keyword : 1})
                    iterForPattern = len(keyword) - 1 
                    iterForText += len(keyword)
                elif (clean_text[iterForText] == keyword[iterForPattern]):
                    iterForText -= 1
                    iterForPattern -= 1
                else : # not the same
                    if (badMatchTable[clean_text[iterForText]] > -1): 
                        if (badMatchTable[clean_text[iterForText]] <= iterForPattern): # occurs again later
                            iterForText += max(1, iterForPattern - badMatchTable[clean_text[iterForText]])
                        else : # not occurs again later
                            iterForText += len(keyword) - iterForPattern
                    else : # not in bad match table
                        iterForText += len(keyword)
                    iterForPattern = len(keyword) - 1 # go back to the last

    return result


if __name__ == "__main__":
    print(boyerMooreMatch("hayo apa hayo", ["ayo", "a"]))
