class SudokuSolver:
    """Solver logic from http://norvig.com/sudoku.html"""

    def __init__(self, solve):
        self.grid = ''
        self.grid_dict = dict()

        self.solve = solve
        self.next_value = None

        self.print_on = True

        self.digits = '123456789'
        self.rows = 'ABCDEFGHI'
        self.cols = self.digits

        self.squares = self.cross(self.rows, self.cols)
        self.unitlist = ([self.cross(self.rows, c) for c in self.cols] +
                [self.cross(r, self.cols) for r in self.rows] +
                [self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.squares)
        self.peers = dict((s, set(sum(self.units[s], []))-set([s])) for s in self.squares)

    def run(self, data):
        self.grid = data
        # self.grid = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'

        if self.print_on:
            self.parse_grid()
            self.display()
        else:
            if not self.parse_grid():
                return data, False

        return self.grid, True, self.next_value

    @staticmethod
    def cross(a, b):
        """Cross product of elements in A and elements in B."""
        return [aa+bb for aa in a for bb in b]

    def parse_grid(self):
        """Convert grid to a dict of possible values, {square: digits}, or
        return False if a contradiction is detected."""
        # To start, every square can be any digit; then assign values from the grid.
        values = dict((s, self.digits) for s in self.squares)
        for s, d in self.grid_values().items():
            if self.solve:
                if d in self.digits and not self.assign(values, s, d):
                    return False
            else:
                if d in self.digits:
                    values[s] = d
                else:
                    values[s] = ''

        self.grid = values
        return True

    def grid_values(self):
        """Convert grid into a dict of {square: char} with '0' or '.' for empties."""
        chars = [c for c in self.grid if c in self.digits or c in '0.']
        assert len(chars) == 81
        return dict(zip(self.squares, chars))

    def assign(self, values, s, d):
        """Eliminate all the other values (except d) from values[s] and propagate.
        Return values, except return False if a contradiction is detected."""
        other_values = values[s].replace(d, '')

        if all(self.eliminate(values, s, d2) for d2 in other_values):
            return values
        else:
            return False

    def eliminate(self, values, s, d):
        """Eliminate d from values[s]; propagate when values or places <= 2.
        Return values, except return False if a contradiction is detected."""
        if d not in values[s]:
            # Already eliminated
            return values
        values[s] = values[s].replace(d, '')

        # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
        if len(values[s]) == 0:
            # Contradiction: removed last value
            return False

        elif len(values[s]) == 1:
            d2 = values[s]

            if not all(self.eliminate(values, s2, d2) for s2 in self.peers[s]):
                return False

        # (2) If a unit u is reduced to only one place for a value d, then put it there.
        for u in self.units[s]:
            d_places = [s for s in u if d in values[s]]
            if len(d_places) == 0:
                # Contradiction: no place for this value
                return False

            elif len(d_places) == 1:
                # d can only be in one place in unit; assign it there
                if not self.assign(values, d_places[0], d):
                    return False
                else:
                    # Save this as next solvable digit
                    if not self.next_value:
                        self.next_value = {s: d}
        return values

    def display(self):
        """Display these values as a 2-D grid."""
        values = self.grid
        width = 1+max(len(values[s]) for s in self.squares)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.rows:
            print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in self.cols))
            if r in 'CF':
                print(line)


# grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
# print(SudokuSolver(solve=True).run(grid1))
