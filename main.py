#Needed for deep copying puzzles
import copy

rows = 3
cols = 3

goal_state = [[1,2,3],
              [4,5,6],
              [7,8,0]]

test1 = [[1,2,3],
         [5,0,6],
         [4,7,8]]


def get_mt_heuristic(puzzle):
    heuristic = 0
    for i in range(rows):
        for j in range(cols):
            if puzzle[i][j] != goal_state[i][j] and puzzle[i][j] != 0:
                heuristic += 1
    return heuristic

def get_pos(puzzle, number):
    for row in range(rows):
        for col in range(cols):
            if puzzle[row][col] == tile:
                return (row, col)
    return -1

def get_md_heuristic(puzzle):
    distance = 0
    for i in range((rows*cols)-1):
        currentPos = get_pos(puzzle, i)
        goalPos = get_pos(goal_state, i)
        distance = abs(currentPos[0] - goalPos[0]) + abs(currentPos[1] - goalPos[1])
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


def search(puzzle, heuristic):

def default_run():

def custom_run():




def main():
    print("Welcome to Peter Sullivan's CS170 Project 1. Enter '1' to use one of the puzzles provided in Professor Keogh's handout or '2' to enter your own:")
    mode = input()
    if mode == 1:
        default_run()
    elif mode == 2:
        custom_run()
    else

