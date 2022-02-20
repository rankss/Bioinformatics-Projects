from Error import InvalidMatrixError, InvalidSequenceTypeError
from Sequence import NUCLEOTIDES, AMINO_ACIDS

class Score:
    """_summary_
    """
    def __init__(self, match: int, mismatch: int, existence: int, extension: int, sequenceType):
        self.matrix = None
        self.match = match
        self.mismatch = mismatch
        self.existence = existence
        self.extension = extension
        self.sequenceType = sequenceType
        self.__Construct()
        return

    def __str__(self):
        """Output Format
        =====================
        | GapExistence: -11 |
        | GapExtension: -1  |
        =====================
        |   | A | G | C | T |
        |---|---|---|---|---|
        | A | 1 |-1 |-1 |-1 |
        |---|---|---|---|---|
        | G |-1 | 1 |-1 |-1 |
        |---|---|---|---|---|
        | C |-1 |-1 | 1 |-1 |
        |---|---|---|---|---|
        | T |-1 |-1 |-1 | 1 |
        =====================
        """
        times_across = len(self.sequenceType) + 1
        output = "="*(4*times_across+1) + f"\n| GapExistence: {str(self.existence).rjust(3).ljust(4)}|\n| GapExtension: {str(self.extension).rjust(3).ljust(4)}|\n"
        output += "="*(4*times_across+1) + "\n|   |"
        for hmonomer in self.sequenceType:
            output += f"{hmonomer.rjust(2).ljust(3)}|"
        for vmonomer in self.sequenceType:
            output += "\n" + "|---"*times_across + "|\n" + f"|{vmonomer.rjust(2).ljust(3)}|"
            for hmonomer in self.sequenceType:
                output += f"{str(self.matrix[vmonomer][hmonomer]).rjust(2).ljust(3)}|"
        output += "\n" + "="*(4*times_across+1)
        return output

    def __ValidateMatrix(self):
        size = len(self.matrix.keys())
        if size != len(self.sequenceType):
            raise InvalidMatrixError(f"InvalidMatrixError: Size Given = {size} | Expected = {len(self.sequenceType)}")

        for key in self.matrix.keys():
            if key not in self.sequenceType:
                raise InvalidMatrixError(f"InvalidMatrixError: {key} is not a valid amino acid")

        for monomer in self.sequenceType:
            if monomer not in self.matrix.keys():
                raise InvalidMatrixError(f"InvalidMatrixError: {monomer} is not found in matrix")
        return
    
    def __Construct(self):
        if self.sequenceType not in [NUCLEOTIDES, AMINO_ACIDS]:
            raise InvalidSequenceTypeError()

        self.matrix = {}
        for vmonomer in self.sequenceType:
            self.matrix[vmonomer] = {}
            for hmonomer in self.sequenceType:
                if vmonomer == hmonomer:
                    self.matrix[vmonomer][hmonomer] = self.match
                else:
                    self.matrix[vmonomer][hmonomer] = self.mismatch
                    
        self.existence = -abs(self.existence)
        self.extension = -abs(self.extension)
        return
    
    def Matrix(self, matrix: dict):
        self.matrix = matrix
        self.__ValidateMatrix()
        return

# Constants
EXAMPLE_MATRIX = {
    'A': {'A': 1, 'G': 0, 'C': 0, 'T': 0},
    'G': {'A': 0, 'G': 1, 'C': 0, 'T': 0},
    'C': {'A': 0, 'G': 0, 'C': 1, 'T': 0},
    'T': {'A': 0, 'G': 0, 'C': 0, 'T': 1}
}

BLOSUM62 = {
    "A":{"A":  4, "R": -1, "N": -2, "D": -2, "C":  0, "Q": -1, "E": -1, "G":  0, "H": -2, "I": -1, "L": -1, "K": -1, "M": -1, "F": -2, "P": -1, "S":  1, "T":  0, "W": -3, "Y": -2, "V":  0, "B": -2, "Z": -1, "X":  0, "*": -4}, 
    "R":{"A": -1, "R":  5, "N":  0, "D": -2, "C": -3, "Q":  1, "E":  0, "G": -2, "H":  0, "I": -3, "L": -2, "K":  2, "M": -1, "F": -3, "P": -2, "S": -1, "T": -1, "W": -3, "Y": -2, "V": -3, "B": -1, "Z":  0, "X": -1, "*": -4}, 
    "N":{"A": -2, "R":  0, "N":  6, "D":  1, "C": -3, "Q":  0, "E":  0, "G":  0, "H":  1, "I": -3, "L": -3, "K":  0, "M": -2, "F": -3, "P": -2, "S":  1, "T":  0, "W": -4, "Y": -2, "V": -3, "B":  3, "Z":  0, "X": -1, "*": -4}, 
    "D":{"A": -2, "R": -2, "N":  1, "D":  6, "C": -3, "Q":  0, "E":  2, "G": -1, "H": -1, "I": -3, "L": -4, "K": -1, "M": -3, "F": -3, "P": -1, "S":  0, "T": -1, "W": -4, "Y": -3, "V": -3, "B":  4, "Z":  1, "X": -1, "*": -4}, 
    "C":{"A":  0, "R": -3, "N": -3, "D": -3, "C":  9, "Q": -3, "E": -4, "G": -3, "H": -3, "I": -1, "L": -1, "K": -3, "M": -1, "F": -2, "P": -3, "S": -1, "T": -1, "W": -2, "Y": -2, "V": -1, "B": -3, "Z": -3, "X": -2, "*": -4}, 
    "Q":{"A": -1, "R":  1, "N":  0, "D":  0, "C": -3, "Q":  5, "E":  2, "G": -2, "H":  0, "I": -3, "L": -2, "K":  1, "M":  0, "F": -3, "P": -1, "S":  0, "T": -1, "W": -2, "Y": -1, "V": -2, "B":  0, "Z":  3, "X": -1, "*": -4}, 
    "E":{"A": -1, "R":  0, "N":  0, "D":  2, "C": -4, "Q":  2, "E":  5, "G": -2, "H":  0, "I": -3, "L": -3, "K":  1, "M": -2, "F": -3, "P": -1, "S":  0, "T": -1, "W": -3, "Y": -2, "V": -2, "B":  1, "Z":  4, "X": -1, "*": -4}, 
    "G":{"A":  0, "R": -2, "N":  0, "D": -1, "C": -3, "Q": -2, "E": -2, "G":  6, "H": -2, "I": -4, "L": -4, "K": -2, "M": -3, "F": -3, "P": -2, "S":  0, "T": -2, "W": -2, "Y": -3, "V": -3, "B": -1, "Z": -2, "X": -1, "*": -4}, 
    "H":{"A": -2, "R":  0, "N":  1, "D": -1, "C": -3, "Q":  0, "E":  0, "G": -2, "H":  8, "I": -3, "L": -3, "K": -1, "M": -2, "F": -1, "P": -2, "S": -1, "T": -2, "W": -2, "Y":  2, "V": -3, "B":  0, "Z":  0, "X": -1, "*": -4}, 
    "I":{"A": -1, "R": -3, "N": -3, "D": -3, "C": -1, "Q": -3, "E": -3, "G": -4, "H": -3, "I":  4, "L":  2, "K": -3, "M":  1, "F":  0, "P": -3, "S": -2, "T": -1, "W": -3, "Y": -1, "V":  3, "B": -3, "Z": -3, "X": -1, "*": -4}, 
    "L":{"A": -1, "R": -2, "N": -3, "D": -4, "C": -1, "Q": -2, "E": -3, "G": -4, "H": -3, "I":  2, "L":  4, "K": -2, "M":  2, "F":  0, "P": -3, "S": -2, "T": -1, "W": -2, "Y": -1, "V":  1, "B": -4, "Z": -3, "X": -1, "*": -4}, 
    "K":{"A": -1, "R":  2, "N":  0, "D": -1, "C": -3, "Q":  1, "E":  1, "G": -2, "H": -1, "I": -3, "L": -2, "K":  5, "M": -1, "F": -3, "P": -1, "S":  0, "T": -1, "W": -3, "Y": -2, "V": -2, "B":  0, "Z":  1, "X": -1, "*": -4}, 
    "M":{"A": -1, "R": -1, "N": -2, "D": -3, "C": -1, "Q":  0, "E": -2, "G": -3, "H": -2, "I":  1, "L":  2, "K": -1, "M":  5, "F":  0, "P": -2, "S": -1, "T": -1, "W": -1, "Y": -1, "V":  1, "B": -3, "Z": -1, "X": -1, "*": -4}, 
    "F":{"A": -2, "R": -3, "N": -3, "D": -3, "C": -2, "Q": -3, "E": -3, "G": -3, "H": -1, "I":  0, "L":  0, "K": -3, "M":  0, "F":  6, "P": -4, "S": -2, "T": -2, "W":  1, "Y":  3, "V": -1, "B": -3, "Z": -3, "X": -1, "*": -4}, 
    "P":{"A": -1, "R": -2, "N": -2, "D": -1, "C": -3, "Q": -1, "E": -1, "G": -2, "H": -2, "I": -3, "L": -3, "K": -1, "M": -2, "F": -4, "P":  7, "S": -1, "T": -1, "W": -4, "Y": -3, "V": -2, "B": -2, "Z": -1, "X": -2, "*": -4}, 
    "S":{"A":  1, "R": -1, "N":  1, "D":  0, "C": -1, "Q":  0, "E":  0, "G":  0, "H": -1, "I": -2, "L": -2, "K":  0, "M": -1, "F": -2, "P": -1, "S":  4, "T":  1, "W": -3, "Y": -2, "V": -2, "B":  0, "Z":  0, "X":  0, "*": -4}, 
    "T":{"A":  0, "R": -1, "N":  0, "D": -1, "C": -1, "Q": -1, "E": -1, "G": -2, "H": -2, "I": -1, "L": -1, "K": -1, "M": -1, "F": -2, "P": -1, "S":  1, "T":  5, "W": -2, "Y": -2, "V":  0, "B": -1, "Z": -1, "X":  0, "*": -4}, 
    "W":{"A": -3, "R": -3, "N": -4, "D": -4, "C": -2, "Q": -2, "E": -3, "G": -2, "H": -2, "I": -3, "L": -2, "K": -3, "M": -1, "F":  1, "P": -4, "S": -3, "T": -2, "W": 11, "Y":  2, "V": -3, "B": -4, "Z": -3, "X": -2, "*": -4}, 
    "Y":{"A": -2, "R": -2, "N": -2, "D": -3, "C": -2, "Q": -1, "E": -2, "G": -3, "H":  2, "I": -1, "L": -1, "K": -2, "M": -1, "F":  3, "P": -3, "S": -2, "T": -2, "W":  2, "Y":  7, "V": -1, "B": -3, "Z": -2, "X": -1, "*": -4}, 
    "V":{"A":  0, "R": -3, "N": -3, "D": -3, "C": -1, "Q": -2, "E": -2, "G": -3, "H": -3, "I":  3, "L":  1, "K": -2, "M":  1, "F": -1, "P": -2, "S": -2, "T":  0, "W": -3, "Y": -1, "V":  4, "B": -3, "Z": -2, "X": -1, "*": -4}, 
    "B":{"A": -2, "R": -1, "N":  3, "D":  4, "C": -3, "Q":  0, "E":  1, "G": -1, "H":  0, "I": -3, "L": -4, "K":  0, "M": -3, "F": -3, "P": -2, "S":  0, "T": -1, "W": -4, "Y": -3, "V": -3, "B":  4, "Z":  1, "X": -1, "*": -4}, 
    "Z":{"A": -1, "R":  0, "N":  0, "D":  1, "C": -3, "Q":  3, "E":  4, "G": -2, "H":  0, "I": -3, "L": -3, "K":  1, "M": -1, "F": -3, "P": -1, "S":  0, "T": -1, "W": -3, "Y": -2, "V": -2, "B":  1, "Z":  4, "X": -1, "*": -4}, 
    "X":{"A":  0, "R": -1, "N": -1, "D": -1, "C": -2, "Q": -1, "E": -1, "G": -1, "H": -1, "I": -1, "L": -1, "K": -1, "M": -1, "F": -1, "P": -2, "S":  0, "T":  0, "W": -2, "Y": -1, "V": -1, "B": -1, "Z": -1, "X": -1, "*": -4}, 
    "*":{"A": -4, "R": -4, "N": -4, "D": -4, "C": -4, "Q": -4, "E": -4, "G": -4, "H": -4, "I": -4, "L": -4, "K": -4, "M": -4, "F": -4, "P": -4, "S": -4, "T": -4, "W": -4, "Y": -4, "V": -4, "B": -4, "Z": -4, "X": -4, "*":  1} 
}