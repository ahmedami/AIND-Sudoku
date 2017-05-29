import operator
import logging
import time
assignments = []
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """
       basically search for a two boxes with the same value 'the value  should be 2 characher' in one unit and remove its values from the other boxes in the unit
       Args:
           A grid in dictionary form .
       Returns:
           A grid in dictionary form
       """
    start_time = int(round(time.time() * 1000))
    logging.info('starting naked twins')

    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    if values is False:
        return False
    #iterate over all the unites
    for unit in unitlist:
        #iterate overall the boxes in each unit first pointer
        for box in unit:
            # get the first pointer value
            value = values[box]
            #ccontinue if it's more than 2 character
            if len(value) != 2:
                continue
            #iterate over all boxes in the unit with second pointer
            for box2 in unit:
                # continue if it point to itself .
                if box == box2:
                    continue
                # get the second pointer value
                value2 = values[box2]
                # check naked twin condition
                is_naked_twin = value==value2 or value[1]+value[0]==value2
                if is_naked_twin and len(value2)==2:
                    #iterate over all boxes in the same unit with a third pointer
                    for box3 in unit:
                        #continue if it point to one of the naked twin pointer
                        if box3 == box2 or box3 == box:
                            continue
                        # iterate over each charachter in naked twin value
                        for c in value:
                            # remove that charachter from any box in the unit
                            if len(values[box3]) > 1 and c in values[box3]:
                                values[box3]=values[box3].replace(c,"")
                # check hidden twin
                elif value in value2 and len(value2) > 2:
                    # create flag to detect hidden twin
                    hidden_twin = True
                    for box3 in unit:
                        if not hidden_twin:
                            break
                        # continue if it point to one of the naked twin pointer
                        if box3 == box2 or box3 == box :
                            continue
                        # iterate over each charachter in naked twin value
                        for c in value:
                            # remove that character from any box in the unit
                            if c in values[box3]:
                                hidden_twin = False
                                break
                    if hidden_twin:
                        values[box2] = value

    #sort the values by the key to pass the test case
    values = dict(sorted(values.items(), key=operator.itemgetter(0)))
    time_taken = int(round(time.time() * 1000))-start_time
    logging.info('Finish naked twins in: '+str(time_taken)+ ' millisec')
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Iterate over all boxes, and remove the one value box from other boxes values .
    Input: dictionary form.
    Output: dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    """
    Iterate over all boxes, and asign the values that only fit in one box to that box.
    Input: dictionary form.
    Output: dictionary form.
     """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    basically apply all propagation constraints techniques untill over and over untill we solve it or there is nothing to do more.
    Input: dictionary form.
    Output: dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    use a Depth first search to try to draw a tree of possibilities untill we found out which road will solve the problem .
    Input: dictionary form.
    Output: dictionary form.
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values=grid_values(grid)
    values=search(values)
    return values



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #display(solve(diag_sudoku_grid))
    display(naked_twins({"G7": "1234568", "G6": "9", "G5": "35678", "G4": "23678", "G3":
"245678", "G2": "123568", "G1": "1234678", "G9": "12345678", "G8":
"1234567", "C9": "13456", "C8": "13456", "C3": "4678", "C2": "68",
"C1": "4678", "C7": "13456", "C6": "368", "C5": "2", "A4": "5", "A9":
"2346", "A8": "2346", "F1": "123689", "F2": "7", "F3": "25689", "F4":
"23468", "F5": "1345689", "F6": "23568", "F7": "1234568", "F8":
"1234569", "F9": "1234568", "B4": "46", "B5": "46", "B6": "1", "B7":
"7", "E9": "12345678", "B1": "5", "B2": "2", "B3": "3", "C4": "9",
"B8": "8", "B9": "9", "I9": "1235678", "I8": "123567", "I1": "123678",
"I3": "25678", "I2": "123568", "I5": "35678", "I4": "23678", "I7":
"9", "I6": "4", "A1": "2468", "A3": "1", "A2": "9", "A5": "3468",
"E8": "12345679", "A7": "2346", "A6": "7", "E5": "13456789", "E4":
"234678", "E7": "1234568", "E6": "23568", "E1": "123689", "E3":
"25689", "E2": "123568", "H8": "234567", "H9": "2345678", "H2":
"23568", "H3": "2456789", "H1": "2346789", "H6": "23568", "H7":
"234568", "H4": "1", "H5": "35678", "D8": "1235679", "D9": "1235678",
"D6": "23568", "D7": "123568", "D4": "23678", "D5": "1356789", "D2":
"4", "D3": "25689", "D1": "123689"}))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
