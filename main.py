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

