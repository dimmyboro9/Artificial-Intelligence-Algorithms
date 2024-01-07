import sys
import time
import pycosat
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, \
    QPushButton, QFrame, QComboBox, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt

SUDOKU_SIZE = 9
BLOCK_SIZE = 3
DOMAINS = {1, 2, 3, 4, 5, 6, 7, 8, 9}


def encode_sudoku_as_cnf(grid):
    clauses = []
    variables = [[[(i, j, k) for k in range(1, 10)] for j in range(9)] for i in range(9)]

    # Rule 1: Each cell must have exactly one value
    for i in range(SUDOKU_SIZE):
        for j in range(SUDOKU_SIZE):
            clauses.append([to_variable(variables[i][j][k]) for k in range(9)])
            for k1 in range(SUDOKU_SIZE - 1):
                for k2 in range(k1 + 1, SUDOKU_SIZE):
                    clauses.append([-to_variable(variables[i][j][k1]), -to_variable(variables[i][j][k2])])

    # Rule 2: Each value must appear exactly once in each row
    for i in range(SUDOKU_SIZE):
        for k in range(SUDOKU_SIZE):
            clauses.append([to_variable(variables[i][j][k]) for j in range(9)])
            for j1 in range(SUDOKU_SIZE - 1):
                for j2 in range(j1 + 1, SUDOKU_SIZE):
                    clauses.append([-to_variable(variables[i][j1][k]), -to_variable(variables[i][j2][k])])

    # Rule 3: Each value must appear exactly once in each column
    for j in range(SUDOKU_SIZE):
        for k in range(SUDOKU_SIZE):
            clauses.append([to_variable(variables[i][j][k]) for i in range(9)])
            for i1 in range(SUDOKU_SIZE - 1):
                for i2 in range(i1 + 1, SUDOKU_SIZE):
                    clauses.append([-to_variable(variables[i1][j][k]), -to_variable(variables[i2][j][k])])

    # Rule 4: Each value must appear exactly once in each 3x3 box
    for r in range(BLOCK_SIZE):
        for c in range(BLOCK_SIZE):
            for k in range(SUDOKU_SIZE):
                clauses.append([to_variable(variables[i][j][k])
                                for i in range(3 * r, 3 * (r + 1)) for j in range(3 * c, 3 * (c + 1))])
                for i1 in range(BLOCK_SIZE * r, BLOCK_SIZE * (r + 1)):
                    for j1 in range(BLOCK_SIZE * c, BLOCK_SIZE * (c + 1)):
                        for i2 in range(i1, BLOCK_SIZE * (r + 1)):
                            for j2 in range(j1 + 1, BLOCK_SIZE * (c + 1)):
                                clauses.append([-to_variable(variables[i1][j1][k]), -to_variable(variables[i2][j2][k])])

    # Rule 5: Add clauses to fix the initial values in the puzzle
    for i in range(SUDOKU_SIZE):
        for j in range(SUDOKU_SIZE):
            val = grid[i][j]
            if val != 0:
                clauses.append([to_variable(variables[i][j][val - 1])])
    return clauses


def to_variable(var):
    return SUDOKU_SIZE ** 2 * var[0] + SUDOKU_SIZE * var[1] + var[2]  # non-zero integer expected


def extract_solution(solution):
    grid = [[0] * SUDOKU_SIZE for _ in range(SUDOKU_SIZE)]
    for var in solution:
        if var > 0:
            i, j, k = from_variable(var)
            grid[i][j] = k + 1
    return grid


def from_variable(var):
    var -= 1
    k = var % 9
    var //= 9
    j = var % 9
    var //= 9
    i = var
    return i, j, k


class CSudokuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.grid = QGridLayout()
        self.grid.setSpacing(1)
        central_widget = QWidget()
        central_widget.setLayout(self.grid)
        self.setCentralWidget(central_widget)
        self.entries = []
        self.vis = 0
        self.par = 0
        self.init_ui()

    def init_ui(self):
        for i in range(SUDOKU_SIZE):
            row_entries = []
            for j in range(SUDOKU_SIZE):
                entry = QLineEdit(self)
                entry.setFixedSize(50, 50)
                entry.setAlignment(Qt.AlignCenter)
                entry.textChanged.connect(self.treat_entry)
                self.grid.addWidget(entry, i, j)
                row_entries.append(entry)

                if j > 0 and j % BLOCK_SIZE == 0:
                    line = QFrame(self)
                    line.setFrameShape(QFrame.VLine)
                    self.grid.addWidget(line, i, j)

            if i < SUDOKU_SIZE - 1 and i % BLOCK_SIZE == 2:
                line = QFrame(self)
                line.setFrameShape(QFrame.HLine)
                self.grid.addWidget(line, i, 0, 2, SUDOKU_SIZE)

            self.entries.append(row_entries)

        combo_box_vis = QComboBox(self)
        combo_box_vis.addItem("Without visualisation")
        combo_box_vis.addItem("Show visualisation")
        combo_box_vis.setCurrentIndex(0)
        combo_box_vis.currentIndexChanged.connect(self.handle_option_vis)
        self.grid.addWidget(combo_box_vis, SUDOKU_SIZE, 0, 1, SUDOKU_SIZE // 2)

        combo_box_par = QComboBox(self)
        combo_box_par.addItem("CSP paradigm")
        combo_box_par.addItem("SAT paradigm")
        combo_box_par.addItem("Simple backtracking")
        combo_box_par.setCurrentIndex(0)
        combo_box_par.currentIndexChanged.connect(self.handle_option_par)
        self.grid.addWidget(combo_box_par, SUDOKU_SIZE, SUDOKU_SIZE // 2, 1, SUDOKU_SIZE)

        solve_button = QPushButton("Solve", self)
        solve_button.clicked.connect(self.solve_sudoku)
        self.grid.addWidget(solve_button, SUDOKU_SIZE + 1, 0, 1, SUDOKU_SIZE)

        reset_button = QPushButton("Reset", self)
        reset_button.clicked.connect(self.reset_sudoku)
        self.grid.addWidget(reset_button, SUDOKU_SIZE + 2, 0, 1, SUDOKU_SIZE)

        cell_style = """
                    QLineEdit {
                        background-color: #FDFDFD;
                        border: 1px solid #CCCCCC;
                        font-size: 24px;
                    }
                """
        for row_entries in self.entries:
            for entry in row_entries:
                entry.setStyleSheet(cell_style)

        theme = """
                    QPushButton {
                        background-color: #EFEFEF;
                        color: #333333;
                        border: 2px solid #CCCCCC;
                        padding: 8px 16px;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: #DDDDDD;
                    }
                    QPushButton:pressed {
                        background-color: #BBBBBB;
                    }
                """
        solve_button.setStyleSheet(theme)
        reset_button.setStyleSheet(theme)

    @pyqtSlot(str)
    def treat_entry(self, text):
        sender = self.sender()
        if text.isdigit() and text[-1] != "0" and self.check_rules(text):
            sender.setText(text[-1])
        elif text == "":
            sender.setText("")
        else:
            sender.setText(text[:-1])

    def check_rules(self, text):
        digit = int(text[-1])
        row, col = self.get_widget_position(self.sender())
        sudoku_grid = self.get_sudoku_grid()
        for j in range(len(sudoku_grid)):
            if sudoku_grid[row][j] == digit and j != col:
                return False

        for i in range(len(sudoku_grid)):
            if sudoku_grid[i][col] == digit and i != row:
                return False

        block_start_row = (row // BLOCK_SIZE) * BLOCK_SIZE
        block_start_col = (col // BLOCK_SIZE) * BLOCK_SIZE
        for i in range(block_start_row, block_start_row + BLOCK_SIZE):
            for j in range(block_start_col, block_start_col + BLOCK_SIZE):
                if sudoku_grid[i][j] == digit and (i != row or j != col):
                    return False
        return True

    def get_sudoku_grid(self):
        grid = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                text = entry.text()
                if text.isdigit():
                    row.append(int(text))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def keyPressEvent(self, event):
        key = event.key()
        current_widget = self.focusWidget()

        if isinstance(current_widget, QLineEdit):
            row, col = self.get_widget_position(current_widget)
            if key == Qt.Key_Up:  # perhaps adding left and right arrows
                row = (row - 1) % SUDOKU_SIZE
            elif key == Qt.Key_Down:
                row = (row + 1) % SUDOKU_SIZE

            next_widget = self.entries[row][col]
            next_widget.setFocus(Qt.TabFocusReason)

    def get_widget_position(self, widget):
        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                if entry is widget:
                    return i, j
        return -1, -1

    @pyqtSlot(int)
    def handle_option_vis(self, index):
        self.vis = index

    @pyqtSlot(int)
    def handle_option_par(self, index):
        self.par = index

    @pyqtSlot()
    def solve_sudoku(self):
        start_time = time.time()
        grid = self.get_sudoku_grid()
        if self.par == 1:
            is_solvable = self.sat(grid)
        else:
            sudoku_solver = CSudokuSolver(self.vis)
            is_solvable = True

            for i, row in enumerate(grid):
                for j, cell in enumerate(row):
                    if cell != 0:
                        is_solvable, tmp = sudoku_solver.assign_dom_to_var(cell, i, j)
                        if not is_solvable:
                            break

            if is_solvable:
                if self.par == 0:
                    is_solvable = sudoku_solver.opt_backtracking(self.entries)
                else:
                    is_solvable = sudoku_solver.backtracking(self.entries)
        end_time = time.time()

        if not is_solvable:
            QMessageBox.critical(None, "Unsolvable sudoku", "This sudoku is unsolvable")
        elif not self.vis:
            QMessageBox.information(None, "Execution time of a program",
                                    f"Duration: {end_time - start_time:.3f} seconds")

    @pyqtSlot()
    def reset_sudoku(self):
        for row_entries in self.entries:
            for entry in row_entries:
                entry.setText("")

    def sat(self, grid):
        cnf = encode_sudoku_as_cnf(grid)
        solution = pycosat.solve(cnf)
        if solution == "UNSAT":
            return False

        new_grid = extract_solution(solution)
        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                entry.setText(str(new_grid[i][j]))
        return True


class CSudokuSolver:
    def __init__(self, vis):
        self.csp = {(0, 0): (set(), DOMAINS.copy())}  # represent csp as a graph
        for row in range(SUDOKU_SIZE):
            for col in range(SUDOKU_SIZE):
                self.add_neighbours(row, col)
        self.empty_cells = SUDOKU_SIZE ** 2
        self.vis = vis

    def add_neighbours(self, row, col):
        for idx in range(SUDOKU_SIZE):
            if idx > col:
                self.add_to_graph(row, col, row, idx)

            if idx > row:
                self.add_to_graph(row, col, idx, col)

        block_start_row = (row // BLOCK_SIZE) * BLOCK_SIZE
        block_start_col = (col // BLOCK_SIZE) * BLOCK_SIZE
        for i in range(block_start_row, block_start_row + BLOCK_SIZE):
            for j in range(block_start_col, block_start_col + BLOCK_SIZE):
                if i < row and j != col:
                    self.add_to_graph(row, col, i, j)

    def add_to_graph(self, row, col, i, j):
        self.csp[(row, col)][0].add((i, j))
        if (i, j) not in self.csp:
            self.csp[(i, j)] = (set(), DOMAINS.copy())
        self.csp[(i, j)][0].add((row, col))

    def assign_dom_to_var(self, val, row, col):
        modified_neighbours = set()
        self.csp[(row, col)][1].clear()
        self.empty_cells -= 1

        for neighbour in self.csp[(row, col)][0]:
            if val in self.csp[neighbour][1]:
                self.csp[neighbour][1].remove(val)
                modified_neighbours.add(neighbour)
                if not len(self.csp[neighbour][1]):
                    return False, modified_neighbours
        return True, modified_neighbours

    def remove_dom_from_var(self, val, row, col, prev_domains, neighbours):
        self.csp[(row, col)][1].update(prev_domains.copy())
        self.empty_cells += 1
        for neighbour in neighbours:
            self.csp[neighbour][1].add(val)

    def opt_backtracking(self, entries):
        if not self.empty_cells:
            return True

        # heuristic for finding out which variable to select - minimum remaining values heuristic (first optimisation)
        var = self.select_variable()
        prev_domains = self.csp[var][1].copy()

        # heuristic for finding out which value to select - least-constraining values heuristic (second optimisation)
        for val in self.select_value(var):
            result, modified_neighbours = self.assign_dom_to_var(val, var[0], var[1])

            if not result:
                self.remove_dom_from_var(val, var[0], var[1], prev_domains, modified_neighbours)

            else:
                entries[var[0]][var[1]].setText(str(val))
                if self.vis:
                    QApplication.processEvents()
                    time.sleep(0.1)
                result = self.opt_backtracking(entries)

                if result:
                    return result

                entries[var[0]][var[1]].setText("")
                if self.vis:
                    QApplication.processEvents()
                    time.sleep(0.1)
                self.remove_dom_from_var(val, var[0], var[1], prev_domains, modified_neighbours)
        return False

    def backtracking(self, entries):
        if not self.empty_cells:
            return True

        row = col = 0
        for key, value in self.csp.items():
            if len(value[1]):
                row = key[0]
                col = key[1]
                break
        prev_domains = self.csp[(row, col)][1].copy()

        for val in prev_domains:
            result, modified_neighbours = self.assign_dom_to_var(val, row, col)

            if not result:
                self.remove_dom_from_var(val, row, col, prev_domains, modified_neighbours)

            else:
                entries[row][col].setText(str(val))
                if self.vis:
                    QApplication.processEvents()
                    time.sleep(0.1)
                result = self.backtracking(entries)

                if result:
                    return result

                entries[row][col].setText("")
                if self.vis:
                    QApplication.processEvents()
                    time.sleep(0.1)
                self.remove_dom_from_var(val, row, col, prev_domains, modified_neighbours)
        return False

    def select_variable(self):
        min_key = None
        min_length = float("inf")

        for key, value in self.csp.items():
            # select the variable that has higher degree if there are some variables that has the smallest number of
            # remaining domains - degree heuristic (third optimisation)
            if len(value[1]) != 0 and (len(value[1]) < min_length or
                                       (len(value[1]) == min_length and
                                        self.amount_of_empty_neighbours(key) >
                                        self.amount_of_empty_neighbours(min_key))):
                min_key = key
                min_length = len(value[1])
        return min_key

    def amount_of_empty_neighbours(self, key):
        key_degree = 0
        for neighbour in self.csp[key][0]:
            if len(self.csp[neighbour][1]) > 0:
                key_degree += 1
        return key_degree

    def select_value(self, var):
        domain_constraints = {}
        for domain in self.csp[var][1]:
            domain_constraints[domain] = self.same_domain_neighbours(var, domain)
        return sorted(domain_constraints, key=lambda k: domain_constraints[k])

    def same_domain_neighbours(self, var, domain):
        amount = 0
        for neighbour in self.csp[var][0]:
            if domain in self.csp[neighbour][1]:
                amount += 1
        return amount


if __name__ == '__main__':
    app = QApplication([])
    window = CSudokuWindow()
    window.show()
    sys.exit(app.exec_())
