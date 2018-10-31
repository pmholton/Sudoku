from itertools import combinations

grid = []
boxes = ((0, 1, 2, 9, 10, 11, 18, 19, 20), (3, 4, 5, 12, 13, 14, 21, 22, 23),
        (6, 7, 8, 15, 16, 17, 24, 25, 26), (27, 28, 29, 36, 37, 38, 45, 46, 47),
        (30, 31, 32, 39, 40, 41, 48, 49, 50), (33, 34, 35, 42, 43, 44, 51, 52, 53),
        (54, 55, 56, 63, 64, 65, 72, 73, 74), (57, 58, 59, 66, 67, 68, 75, 76, 77), 
        (60, 61, 62, 69, 70, 71, 78, 79, 80))
rows = ((0,1,2,3,4,5,6,7,8), (9,10,11,12,13,14,15,16,17), (18,19,20,21,22,23,24,25,26),
       (27,28,29,30,31,32,33,34,35), (36,37,38,39,40,41,42,43,44),
       (45,46,47,48,49,50,51,52,53), (54,55,56,57,58,59,60,61,62),
       (63,64,65,66,67,68,69,70,71), (72,73,74,75,76,77,78,79,80))
cols = ((0,9,18,27,36,45,54,63,72), (1,10,19,28,37,46,55,64,73),
       (2,11,20,29,38,47,56,65,74), (3,12,21,30,39,48,57,66,75),
       (4,13,22,31,40,49,58,67,76), (5,14,23,32,41,50,59,68,77),
       (6,15,24,33,42,51,60,69,78), (7,16,25,34,43,52,61,70,79),
       (8,17,26,35,44,53,62,71,80))
box_rows = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
box_cols = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
candidate_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
global puzzles_solved
puzzles_solved = 0

class Cell():
    # Each sudoku puzzle has 81 Cells which hold a Value and
    # a set of Candidates if it is currently unsolved.
    def __init__(self, value_in):
        self.value = value_in
        self.candidates = set() 

def printGrid(grid_in):
    # Returns the current cell values in a 9x9 array.
    grid = grid_in
    grid_array = []
    for lines in range(9):
        grid_row = []
        for cells in range(9):
            grid_row.append(grid[9*lines + cells].value)
        grid_array.append(grid_row)
    return grid_array

def solved(grid_in):
    # Returns true if the puzzle is solved.
    grid = grid_in
    solved = True
    cell_number = 0
    while cell_number < 81 and solved:
        if grid[cell_number].value == 0:
            solved = False
        cell_number += 1
    return solved

def getHist(grid_in, list_in):
    # Returns a histogram of items in the input list as a dictionary.
    grid = grid_in
    histogram = {}
    for number in list_in:
        if grid[number].value == 0:
            for val in grid[number].candidates:
                histogram[val] = histogram.get(val, 0) + 1
    return histogram

def getRow(index):
    # Returns the row number (0-8) that contains the given index.
    row_num = 0
    for row in rows:
        if index in row:
            return row_num
        row_num += 1
    print("Invalid getRow() index - " + str(index))
    return

def getCol(index):
    # Returns the column number (0-8) that contains the given index.
    col_num = 0
    for col in cols:
        if index in col:
            return col_num
        col_num += 1
    print("Invalid getCol() index - " + str(index))
    return

def getBox(index):
    # Returns the box number (0-8) that contains the given index.
    box_num = 0
    for box in boxes:
        if index in box:
            return box_num
        box_num += 1
    print("Invalid getBox() index - " + str(index))
    return

def fillCandidates(grid_in):
    # Fills in cell candidates using basic row, column, and box logic.
    grid = grid_in
    for cell_number in range(81):
        used_candidates = {0}
        if grid[cell_number].value == 0:
            # Get Row
            row_begin = cell_number - (cell_number % 9)
            row = [grid[row_index].value for row_index in range(row_begin, row_begin + 9)]
            # Get Column
            col_begin = cell_number % 9
            col = [grid[col_index].value for col_index in range(col_begin, col_begin + 81, 9)]
            # Get Box
            row_num = cell_number // 27
            col_num = (cell_number % 9) // 3
            box_num = 3 * row_num + col_num
            box = [grid[box_index].value for box_index in boxes[box_num]]
            # Basic Logic
            used_candidates = set(row) | set(col) | set(box)
            grid[cell_number].candidates = candidate_set - used_candidates
    return grid

def soleCandidate(grid_in):
    # Fills values by travelling cells and filling in
    # cells where there is only one candidate.
    grid = grid_in
    changes = 0
    for cell in grid:
        if cell.value == 0 and len(cell.candidates) == 1:
            temp_candidates = set() | cell.candidates
            cell.value = cell.candidates.pop()
            changes += 1
    # print('Sole Candidates - ' + str(changes))
    return grid

def uniqueCandidate(grid_in):
    # Fills Values by travelling boxes, rows, and columns and filling in
    # cells which have the only instance of a number in that subsquare.
    grid = grid_in
    changes = 0
    changed = False
    times_round = 0
    sets_to_check = boxes + rows + cols
    for list_to_check in sets_to_check:
        times_round += 1
        candidate_hist = getHist(grid, list_to_check)
        for candidate_num in candidate_hist:
            if candidate_hist[candidate_num] == 1:
                for cell_number in list_to_check:
                    if candidate_num in grid[cell_number].candidates:
                        grid[cell_number].value = candidate_num
                        grid[cell_number].candidates = set()
                        changes += 1
                        changed = True
        # When you move from checking boxes to rows or rows to columns,
        # you need to refresh candidates if you've made a change.
        if times_round in (9,18) and changed == True:
            fillCandidates(grid)
            changed = False
    # print('Unique Candidates - ' + str(changes))
    return grid

def nakedSets(grid_in):
    # Removes candidates by finding naked sets in rows, columns, or boxes
    grid = grid_in
    pairs = 0
    trips = 0
    quads = 0
    sets_to_check = rows + cols + boxes
    for list_to_check in sets_to_check:
    	# Checking for pairs
        for pair in combinations(list_to_check, 2):
            if grid[pair[0]].value == 0 and grid[pair[1]].value == 0:
                candidate_pair = grid[pair[0]].candidates | grid[pair[1]].candidates
                if len(candidate_pair) == 2:
                    pairs += 1
                    for cell_number in list_to_check:
                        if cell_number not in pair and grid[cell_number].value == 0:
                            grid[cell_number].candidates = grid[cell_number].candidates - candidate_pair
        # Checking for Triplets
        for trip in combinations(list_to_check, 3):
            if grid[trip[0]].value == 0 and grid[trip[1]].value == 0 and grid[trip[2]].value == 0:
                candidate_trip = grid[trip[0]].candidates | grid[trip[1]].candidates | grid[trip[2]].candidates
                if len(candidate_trip) == 3:
                    trips += 1
                    for cell_number in list_to_check:
                        if cell_number not in trip and grid[cell_number].value == 0:
                            grid[cell_number].candidates = grid[cell_number].candidates - candidate_trip
        # Checking for Quartets
        for quad in combinations(list_to_check, 4):
            if grid[quad[0]].value == 0 and grid[quad[1]].value == 0 and grid[quad[2]].value == 0 and grid[quad[3]].value == 0:
                candidate_quad = grid[quad[0]].candidates | grid[quad[1]].candidates | grid[quad[2]].candidates | grid[quad[3]].candidates
                if len(candidate_quad) == 4:
                    quads += 1
                    for cell_number in list_to_check:
                        if cell_number not in quad and grid[cell_number].value == 0:
                            grid[cell_number].candidates = grid[cell_number].candidates - candidate_quad

    # print('Naked Sets: Pairs - ' + str(pairs) + ', Trios - ' + str(trips) + ', Quads - ' + str(quads))
    return grid

def hiddenSets(grid_in):
    # Removes candidates based on hidden sets found in rows, cols, and boxes
    grid = grid_in
    pairs = 0
    trips = 0
    quads = 0
    sets_to_check = rows + cols + boxes
    for list_to_check in sets_to_check:
        list_hist = getHist(grid, list_to_check)
        # Checking for pairs
        for pair in combinations(list_to_check, 2):
            if grid[pair[0]].value == 0 and grid[pair[1]].value == 0:
                intersect = grid[pair[0]].candidates.intersection(grid[pair[1]].candidates)
                if len(intersect) >= 2:
                    for candidate_pair in combinations(intersect, 2):
                        if list_hist[candidate_pair[0]] == 2 and list_hist[candidate_pair[1]] == 2:
                            new_candidates = set(candidate_pair)
                            grid[pair[0]].candidates = new_candidates
                            grid[pair[1]].candidates = new_candidates
                            pairs += 1
        # Checking for Triplets
        for trip in combinations(list_to_check, 3):
            if grid[trip[0]].value == 0 and grid[trip[1]].value == 0 and grid[trip[2]].value == 0:
                cand_hist = getHist(grid, trip)
                unique_cand = set()
                for num in cand_hist:
                    if cand_hist[num] == list_hist[num]:
                        unique_cand = unique_cand.union({num})
                if len(unique_cand) == 3:
                    trips += 1
                    for cell_number in trip:
                        grid[cell_number].candidates = grid[cell_number].candidates.intersection(unique_cand)
        # Checking for Quartets
        for quad in combinations(list_to_check, 4):
            if grid[quad[0]].value == 0 and grid[quad[1]].value == 0 and grid[quad[2]].value == 0 and grid[quad[3]].value == 0:
                cand_hist = getHist(grid, quad)
                unique_cand = set()
                for num in cand_hist:
                    if cand_hist[num] == list_hist[num]:
                        unique_cand = unique_cand.union({num})
                if len(unique_cand) == 4:
                    quads += 1
                    for cell_number in quad:
                        grid[cell_number].candidates = grid[cell_number].candidates.intersection(unique_cand)
    # print('Hidden Sets: Pairs - ' + str(pairs) + ', Trios - ' + str(trips) + ', Quads - ' + str(quads))
    return grid

def pointingSets(grid_in):
    # Removes candidates traveling box by box, searching box-rows and
    # box-columns to see if all occurrences of a candidate are in that line,
    # then removing that candidate from the greater row or column
    grid = grid_in
    changes = 0
    sudoku_row = 0
    sudoku_col = 0

    for box in boxes:
        box_hist = getHist(grid, box)
        for row in box_rows:
            row_to_check = [box[row[0]], box[row[1]], box[row[2]]]
            row_hist = getHist(grid, row_to_check)
            for num in row_hist:
                if row_hist[num] == box_hist[num]:
                    sudoku_row = getRow(row_to_check[0])
                    for cell_number in rows[sudoku_row]:
                        if cell_number not in row_to_check:
                            if num in grid[cell_number].candidates:
                                grid[cell_number].candidates = grid[cell_number].candidates.difference({num})
                                changes += 1
        for col in box_cols:
            col_to_check = [box[col[0]], box[col[1]], box[col[2]]]
            col_hist = getHist(grid, col_to_check)
            for num in col_hist:
                if col_hist[num] == box_hist[num]:
                    sudoku_col = getCol(col_to_check[0])
                    for cell_number in cols[sudoku_col]:
                        if cell_number not in col_to_check:
                            if num in grid[cell_number].candidates:
                                grid[cell_number].candidates = grid[cell_number].candidates.difference({num})
                                changes += 1
    # print('Pointing Sets - ' + str(changes))
    return grid

def boxLineIntersection(grid_in):
    # Travels line by line, looks to see if all occurences of a 
    # candidate number are in one box, and removes those candidates 
    # from the rest of the box
    grid = grid_in
    sudoku_box = 0
    changes = 0
    for line in (rows + cols):
        line_hist = getHist(grid, line)
        for box_start in [0, 3, 6]:
            list_to_check = [line[box_start], line[box_start + 1], line[box_start + 2]]
            box_hist = getHist(grid, list_to_check)
            for num in box_hist:
                if box_hist[num] == line_hist[num]:
                    sudoku_box = getBox(list_to_check[0])
                    for cell_num in boxes[sudoku_box]:
                        if cell_num not in list_to_check:
                            if num in grid[cell_num].candidates:
                                grid[cell_num].candidates = grid[cell_num].candidates.difference({num})
                                changes += 1
    # print('Box-Line Intersection - ' + str(changes))
    return grid

def xWing(grid_in):
    # Removes candidates according to the x-wing strategy.
    # See http://www.sudokuwiki.org/X_Wing_Strategy
    grid = grid_in
    changes = 0
    for row_combo in combinations(range(9), 2):
        row_a = rows[row_combo[0]]
        row_b = rows[row_combo[1]]
        row_a_hist = getHist(grid, row_a)
        row_b_hist = getHist(grid, row_b)
        for num in row_a_hist:
            if num in row_b_hist and row_a_hist[num] == 2 and row_b_hist[num] == 2:
                matching_cols = []
                for col_num in range(9):
                    if (num in grid[row_a[col_num]].candidates) and (num in grid[row_b[col_num]].candidates):
                        matching_cols.append(col_num)
                if len(matching_cols) == 2:
                    for col_index in matching_cols:
                        col = cols[col_index]
                        for cell_num in col:
                            if (cell_num not in row_a) and (cell_num not in row_b):
                                if num in grid[cell_num].candidates:
                                    grid[cell_num].candidates = grid[cell_num].candidates.difference({num})
                                    changes += 1
    for col_combo in combinations(range(9), 2):
        col_a = cols[col_combo[0]]
        col_b = cols[col_combo[1]]
        col_a_hist = getHist(grid, col_a)
        col_b_hist = getHist(grid,col_b)
        for num in col_a_hist:
            if num in col_b_hist and col_a_hist[num] == 2 and col_b_hist[num] == 2:
                matching_rows = []
                for row_num in range(9):
                    if (num in grid[col_a[row_num]].candidates) and (num in grid[col_b[row_num]].candidates):
                        matching_rows.append(row_num)
                if len(matching_rows) == 2:
                    for row_index in matching_rows:
                        row = rows[row_index]
                        for cell_num in row:
                            if (cell_num not in col_a) and (cell_num not in col_b):
                                if num in grid[cell_num].candidates:
                                    grid[cell_num].candidates = grid[cell_num].candidates.difference({num})
                                    changes += 1
    # print('X-Wing - ' + str(changes))
    return grid

def format_grid(grid_in):
    raw_grid = grid_in
    grid = []
    for i in range(len(raw_grid)):
        for j in range(len(raw_grid[0])):
            grid.append(Cell(raw_grid[i][j]))
    return grid

def solve(grid_in):
    # Solves sudoku puzzles or prints the farthest it can get.
    global puzzles_solved
    solution = True
    grid = format_grid(grid_in)

    while not solved(grid):
        grid = fillCandidates(grid)
        pre_grid = printGrid(grid)
        grid = soleCandidate(grid)
        if pre_grid != printGrid(grid):
            continue
        grid = uniqueCandidate(grid)
        if pre_grid != printGrid(grid):
            continue

        grid = nakedSets(grid)
        grid = soleCandidate(grid)
        if pre_grid != printGrid(grid):
            continue
        grid = uniqueCandidate(grid)
        if pre_grid != printGrid(grid):
            continue

        grid = hiddenSets(grid)
        grid = soleCandidate(grid)
        if pre_grid != printGrid(grid):
            continue
        grid = uniqueCandidate(grid)
        if pre_grid != printGrid(grid):
            continue

        grid = pointingSets(grid)
        grid = soleCandidate(grid)
        if pre_grid != printGrid(grid):
            continue
        grid = uniqueCandidate(grid)
        if pre_grid != printGrid(grid):
            continue

        grid = boxLineIntersection(grid)
        grid = soleCandidate(grid)
        if pre_grid != printGrid(grid):
            continue
        grid = uniqueCandidate(grid)
        if pre_grid != printGrid(grid):
            continue

        grid = xWing(grid)
        grid = soleCandidate(grid)
        if pre_grid != printGrid(grid):
            continue
        grid = uniqueCandidate(grid)
        if pre_grid != printGrid(grid):
            continue

        print('The given sudoku cannot be solved by this program.')
        # for lines in printGrid():
        #     print(lines)
        solution = False
        break

    # for lines in printGrid(grid):
    #     print(lines)
    if solution:
        puzzles_solved += 1
    return solution, printGrid(grid)


grid_temp = []
puzzle_num = 1

if __name__ == '__main__':
    with open('sudoku.txt') as sudoku:
        line_num = 1
        for line in sudoku:
            if line_num % 10 == 1:
                print('\n----==== Sudoku #' + str(puzzle_num) + ' ====----')
                puzzle_num += 1
            else:
                for number in line.strip():
                    grid_temp.append(Cell(int(number)))
                if len(grid_temp) == 81:
                    grid = grid_temp
                    solve(grid)
                    grid_temp = []
            line_num += 1
    print(str(puzzles_solved) + ' Puzzles were solved.')