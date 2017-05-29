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
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    if values is False:
        return False
    #iterate over all the unites
    for unit in unitlist:
        #save the boxes with lenght two for the current unit
        tower_boxes={}
        #save the twins keys for the current unit, key is the first box , value is the second box
        twin_boxes = {}
        #iterate overall the boxes in the current unit
        for box in unit:
            # get all boxes with lenght two
            if len(values[box]) == 2:
                tower_boxes[box]=values[box]
        #detect twins
        for key, val in tower_boxes.items():
            for key1, val1 in tower_boxes.items():
                is_twin = val1==val or val1 == val[1]+val[0]
                if key1 != key and is_twin:
                    twin_boxes[key]=key1
        # iterate over the unit to remove the twin value from other boxes
        for key, key1 in twin_boxes.items():
            for box in unit:
                #make sure that we didn't remove the twin value itself
                if box != key and box != key1:
                    for c in values[key]:
                        values[box]=values[box].replace(c,"")
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
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
