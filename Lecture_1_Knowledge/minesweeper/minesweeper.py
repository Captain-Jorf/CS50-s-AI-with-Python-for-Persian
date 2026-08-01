import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count and self.count != 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbors = set()
        i, j = cell
        c = count
        for r in range(i - 1, i + 2):
            for k in range(j - 1, j + 2):
                if (r, k) == cell:
                    continue
                if 0 <= r < self.height and 0 <= k < self.width:
                    if (r, k) in self.mines:
                        c -= 1
                    elif (r, k) not in self.safes:
                        neighbors.add((r, k))

        if neighbors:
            self.knowledge.append(Sentence(neighbors, c))

        changed = True
        while changed:
            changed = False

            safes_found = set()
            mines_found = set()
            for s in self.knowledge:
                safes_found |= s.known_safes()
                mines_found |= s.known_mines()

            for x in safes_found:
                if x not in self.safes:
                    self.mark_safe(x)
                    changed = True
            for x in mines_found:
                if x not in self.mines:
                    self.mark_mine(x)
                    changed = True

            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

            new_sentences = []
            for a in self.knowledge:
                for b in self.knowledge:
                    if a is b:
                        continue
                    if a.cells and b.cells and a.cells < b.cells:
                        diff_cells = b.cells - a.cells
                        diff_count = b.count - a.count
                        new_s = Sentence(diff_cells, diff_count)
                        if new_s not in self.knowledge and new_s not in new_sentences:
                            new_sentences.append(new_s)

            if new_sentences:
                self.knowledge.extend(new_sentences)
                changed = True

    def make_safe_move(self):
        for c in self.safes:
            if c not in self.moves_made:
                return c
        return None

    def make_random_move(self):
        choices = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    choices.append(cell)
        if not choices:
            return None
        return random.choice(choices)
