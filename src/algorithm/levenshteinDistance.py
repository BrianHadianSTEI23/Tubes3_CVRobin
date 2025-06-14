
# specification : insert, subsitute, remove

class LevenshteinCalculator:
    "pake pendekatan dp biar ga bruteforce"

    def __init__(self, s1: str, s2: str):
        self.s1 = s1
        self.s2 = s2
        self.lenS1 = len(s1)
        self.lenS2 = len(s2)
        self.dpMatrix = []
    
    def calculate(self) -> int:
        self.dpMatrix = [[0 for _ in range(self.lenS2 + 1)] for _ in range(self.lenS1 + 1)]

        "isi cost"
        for j in range(self.lenS2 + 1):
            self.dpMatrix[0][j] = j

        for i in range(self.lenS1 + 1):
            self.dpMatrix[i][0] = i

        for i in range(1, self.lenS1 + 1):
            for j in range(1, self.lenS2 + 1):
                substitutionCost = 0
                if self.s1[i-1] == self.s2[j-1]:
                    substitutionCost = 0
                else:
                    substitutionCost = 1
                self.dpMatrix[i][j] = min(
                    self.dpMatrix[i-1][j] + 1,
                    self.dpMatrix[i][j-1] + 1,
                    self.dpMatrix[i-1][j-1] + substitutionCost
                )

        # self.printMatrix()
        return self.dpMatrix[self.lenS1][self.lenS2]

    def printMatrix(self):
        print("Matrix LevenShtein: ")
        for row in self.dpMatrix:
            print(row)



def fuzzyMatch(keywords: list[str], text: str, threshold: int) -> int:
    # print(f"Mencari '{keyword}' di dalam teks dengan threshold <= {threshold}...")
    wordsInText = text.lower().split()
    #list buat nyimpen kata yg mungkin cocok
    foundMatches = 0
    
    for word in wordsInText:
        for keyword in keywords:
            calculator = LevenshteinCalculator(keyword.lower(), word)
            distance = calculator.calculate()
            if distance <= threshold:
                print(f"  -> Ditemukan kecocokan: '{word}' (jarak: {distance})")
                foundMatches += 1
            
    return foundMatches

# contoh_teks_cv = "My main skill is programming with javva, jaa, and pythin."
# kata_kunci = ["java"]
# ambang_batas = 2

# kecocokan = fuzzyMatch(kata_kunci, contoh_teks_cv, ambang_batas)
# print(f"\nHasil akhir kata yang cocok: {kecocokan}")