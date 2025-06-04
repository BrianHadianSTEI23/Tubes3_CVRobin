
# specification : insert, subsitute, remove

class Node:

    def __init__(self, name : str, toExpand : list["Node"], value : int, alphabet : list[str]) : 
        self.name = name
        self.toExpand = toExpand
        self.value = value
        self.alphabet = alphabet

    # expand node
    def levenshteinDistance(self, target : str) :
        if (self.name == target) :
            return self.value
        else :
            # insert 
            if len(self.name) < len(target):
                for letter in self.alphabet:
                    for i in range(len(self.name)):
                        newName : str = self.name[:i] + letter + self.name[i:]
                        newValue : int = self.value + 1
                        self.toExpand.append(Node(newName, [], newValue, self.alphabet))
            # delete
            if len(self.name) > 0:
                for i in range(len(self.name)):
                    newName : str = self.name[:i - 1] + self.name[i:]
                    newValue : int = self.value + 1
                    self.toExpand.append(Node(newName, [], newValue, self.alphabet))
            # substitute
            for letter in self.alphabet:
                if letter in self.name:
                    for i in range(len(self.name)):
                        if (letter != self.name[i]) :
                            newName : str = self.name[:i - 1] + letter + self.name[i:]
                            newValue : int = self.value + 1
                            self.toExpand.append(Node(newName, [], newValue, self.alphabet))

            # expand all
            for node in self.toExpand:
                node.levenshteinDistance(target)