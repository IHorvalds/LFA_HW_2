class Automaton():
    def __init__(self, moves, startState, endStates, alphabet):
        self.startState = startState
        self.endStates = endStates
        self.moves = moves
        self.__removeUnreachableStates()
        self.alphabet = alphabet

    def __removeUnreachableStates(self):
        pass

    def __getAlphabet(self) -> set:
        alpha = set()

        for m in self.moves:
            if m[2] != "$":
                alpha.add(m[2])

        return alpha

    def __str__(self):
        s = "Start state: " + str(self.startState) + '\n'
        s += "End states: " + str(self.endStates) + '\n'
        for m in self.moves:
            s += str(m) + '\n'
        return s

    @staticmethod
    def findLambdaClosure(automaton, stateList) -> set:

        closure = set()

        queue = list(stateList)

        while queue:
            currentState = queue.pop(0)

            closure.add(currentState)

            for m in automaton.moves:
                if m[2] == "$" and m[0] == currentState and (m[1] not in closure):
                    queue.append(m[1])

        return closure



def read() -> Automaton:
    with open("input.txt") as f:
        startState = int(f.readline().replace('\n', ''))
        endStates = list(int(x) for x in f.readline().replace('\n', '').split(' '))
        alphabet = f.readline().replace('\n', '').split(' ')
        moves = list(  ( int(line.replace('\n', '').split(' ')[0]), int(line.replace('\n', '').split(' ')[1]), line.replace('\n', '').split(' ')[2] ) for line in f.readlines()  )
        return Automaton(moves, startState, endStates, alphabet)

def hashSet(s): # not an actual hashing function
    return str(s)


def main():
    automaton = read()

    newStatesQueue = []
    newStatesDict = dict()


    firstState = Automaton.findLambdaClosure(automaton, set([automaton.startState]))
    
    newStatesDict[hashSet(firstState)] = {}
    newStatesQueue.append(firstState)

    finalStates = set()

    while newStatesQueue:
        currentStateToVerify = newStatesQueue.pop(0)
        currentStateToVerifyHash = hashSet(currentStateToVerify)

        movesStartingInCurrentStates = list(filter(lambda x: x[0] in currentStateToVerify, automaton.moves))

        for letter in automaton.alphabet:

            possibleMoves = set()
            for m in movesStartingInCurrentStates:
                if m[2] == letter:
                    possibleMoves.add(m[1])

            newStatesDict[currentStateToVerifyHash][letter] = Automaton.findLambdaClosure(automaton, possibleMoves)

            if hashSet(newStatesDict[currentStateToVerifyHash][letter]) not in newStatesDict.keys():
                newStatesQueue.append(newStatesDict[currentStateToVerifyHash][letter])
                newStatesDict[hashSet(newStatesDict[currentStateToVerifyHash][letter])] = {}

    for endState in automaton.endStates:
        for state in newStatesDict.keys():
            if state.find(str(endState)) != -1:
                finalStates.add(state)

    stateNames = {}

    for i, s in enumerate(newStatesDict.keys()):
        stateNames[s] = chr(65 + i)

    moves = []

    for state, possibleMoves in newStatesDict.items():
        for letter, toState in possibleMoves.items():
            moves.append( (stateNames[state], stateNames[hashSet(toState)], letter) )

    finalStatesNames = list(map(lambda state: stateNames[state], list(finalStates)))

    automaton2 = Automaton(moves, stateNames[hashSet(firstState)], finalStatesNames, automaton.alphabet)

    print(automaton2)

if __name__ == "__main__" :
    main()