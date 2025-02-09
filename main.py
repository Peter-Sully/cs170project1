#Needed for deep copying puzzles
import copy
#Used to represent the tree/queue
import heapq

#Class to store nodes in the search queue
class Node:
    def __init__(self, puzzle, g, h):
        self.puzzle = puzzle
        self.g = g
        self.h = h
        self.cost = g+h
    
    def __lt__(self, other):
        return (self.cost) < (other.cost)
    
    def __eq__(self, other):
        return self.puzzle == other.puzzle

#An attempt at generality. There's currently no way to input a bigger puzzle, but modifying these should
#make decent steps towards working with varying size puzzles
rows = 3
cols = 3

#solved puzzle
goal_state = [[1,2,3],
              [4,5,6],
              [7,8,0]]

#puzzles given in the assignment handout
given_puzzles = [[[1,2,3],
                  [4,5,6],
                  [0,7,8]],

                 [[1,2,3],
                  [5,0,6],
                  [4,7,8]],

                 [[1,3,6],
                  [5,0,2],
                  [4,7,8]],
                  
                 [[1,3,6],
                  [5,0,7],
                  [4,8,2]],
                  
                 [[1,6,7],
                  [5,0,3],
                  [4,8,2]],
                  
                 [[7,1,2],
                  [4,8,5],
                  [6,3,0]],
                
                 [[0,7,2],
                  [4,6,1],
                  [3,5,8]]]

#UCS function to pass into search, returns 0 no matter what
def get_uc_heuristic(puzzle):
    return 0

#Function to get Misplaced Tile heuristic in a given puzzle
def get_mt_heuristic(puzzle):
    heuristic = 0
    for i in range(rows):
        for j in range(cols):
            if puzzle[i][j] != goal_state[i][j] and puzzle[i][j] != 0:
                heuristic += 1
    return heuristic

#Function to get current position of a number in a given puzzle
def get_pos(puzzle, number):
    for row in range(rows):
        for col in range(cols):
            if puzzle[row][col] == number:
                return (row, col)
    return -1

#Function to get Manhattan Distance given a puzzle 
def get_md_heuristic(puzzle):
    distance = 0
    for i in range(1, (rows*cols)):
        currentPos = get_pos(puzzle, i)
        goalPos = get_pos(goal_state, i)
        distance += abs(currentPos[0] - goalPos[0]) + abs(currentPos[1] - goalPos[1])
    return distance

#Function to get coordinates of valid moves
def get_moves(puzzle):
    emptyPos = get_pos(puzzle, 0)
    newPos = []
    # Check one spot up
    if emptyPos[0]-1 >= 0:
        newPos.append((emptyPos[0]-1, emptyPos[1]))
    # Check one spot down
    if emptyPos[0]+1 < rows:
        newPos.append((emptyPos[0]+1, emptyPos[1]))
    # Check one spot left
    if emptyPos[1]-1 >= 0:
        newPos.append((emptyPos[0], emptyPos[1]-1))
    # Check one spot right
    if emptyPos[1]+1 < cols:
        newPos.append((emptyPos[0], emptyPos[1]+1))
    return newPos

#Function to make puzzles out of list of moves
def make_moves(puzzle, moves):
    emptyPos = get_pos(puzzle, 0)
    puzzles = []
    for move in moves:
        tempPuzz = copy.deepcopy(puzzle)
        tempPuzz[move[0]][move[1]], tempPuzz[emptyPos[0]][emptyPos[1]] = tempPuzz[emptyPos[0]][emptyPos[1]], tempPuzz[move[0]][move[1]]
        puzzles.append(tempPuzz)
    return puzzles

#function to print out a puzzle
def puzzle_print(puzzle):
    for row in puzzle:
        print(row)

#search function
def search(puzzle, heuristic):
    start = Node(puzzle, 0, heuristic(puzzle))
    tree = []
    heapq.heappush(tree,start)
    nodesExpanded = 0
    maxQueueLength = 1
    visited = {}
    #converting puzzle to a tuple of tuples as lists cannot be dict keys
    visited[tuple(map(tuple, start.puzzle))] = start.cost
    while tree:
        #moved fail state to outside while loop, logically equivalent but just mentioning it here since it deviates from basic search pseudocode
        maxQueueLength = max(len(tree), maxQueueLength)
        currNode = heapq.heappop(tree)
        #output heavily inspired by sample report
        print(f"The best state to expand with a g(n) = {currNode.g} and h(n) = {currNode.h} is:")
        puzzle_print(currNode.puzzle)

        #Check if current state is goal, and if so exit
        if currNode.puzzle == goal_state:
            print("Goal state!\n")
            print(f"Solution depth was {currNode.g}")
            print(f"Number of nodes expanded: {nodesExpanded}")
            print(f"Max queue size = {maxQueueLength}")
            #currently not doing anything with this return value, but could be useful if you were building upon this code
            return currNode
        
        #Current state is not the goal, so expand current state
        nodesExpanded += 1
        moves = get_moves(currNode.puzzle)
        newPuzzles = make_moves(currNode.puzzle, moves)
        
        #Check that all new states either havent been seen before, or are cheaper than their previous occurances
        for puzzle in newPuzzles:
            newG = currNode.g + 1
            newH = heuristic(puzzle)
            #Forgot that these puzzles arent Nodes yet, so I cant use the Node cost data member, womp womp. So calculating it here
            newCost = newG+newH
            puzzleTup = tuple(map(tuple, puzzle))
            if puzzleTup not in visited or newCost < visited[puzzleTup]:
                visited[puzzleTup] = newCost
                newNode = Node(puzzle, newG, newH)
                heapq.heappush(tree, newNode)
    #As previously mentioned, moved from the start of the start of the loop in the pseudocode
    print("Search failed.")
    return

        
        


#Initialize a run using one of the given puzzles
def default_run():
    print("Enter a number from 1-7 to choose one of Dr. Keogh's given puzzles")
    puzzle = int(input())-1
    print("Enter '1' to use uniform cost search, '2' for A* with misplaced tile, or '3' for A* with manhattan distance")
    alg = input()
    if alg == '1':
        search(given_puzzles[puzzle], get_uc_heuristic)
    elif alg == '2':
        search(given_puzzles[puzzle], get_mt_heuristic)
    elif alg == '3':
        search(given_puzzles[puzzle], get_md_heuristic)

#Initialize a run using a user inputted puzzle. Should probably have input filtering, but I'll only add if I have time
def custom_run():
    print("Enter your puzzle, row by row, with 0 representing the blank spot. Press enter once you have finished a row, and leave spaces in between numbers\n")
    print("Row 1:")
    row1 = input()
    print("Row 2:")
    row2 = input()
    print("Row 3:")
    row3 = input()
    puzzle = [list(map(int, row1.split())), list(map(int, row2.split())), list(map(int, row3.split()))]
    print("Enter '1' to use uniform cost search, '2' for A* with misplaced tile, or '3' for A* with manhattan distance")
    alg = input()
    if alg == '1':
        search(puzzle, get_uc_heuristic)
    elif  alg == '2':
        search(puzzle, get_mt_heuristic)
    elif alg == '3':
        search(puzzle, get_md_heuristic)


#Begin interface
def main():
    print("Welcome to Peter Sullivan's CS170 Project 1. Enter '1' to use one of the puzzles provided in Dr. Keogh's handout or '2' to enter your own:")
    mode = input()
    if mode == '1':
        default_run()
    elif mode == '2':
        custom_run()
    return

main()