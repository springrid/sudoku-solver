from flask import Flask, render_template, request, redirect, url_for
from sudoku_solver import SudokuSolver

app = Flask(__name__)
app._static_folder = 'static'

sudoku_solver = SudokuSolver(solve=True)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve():
    sudoku_data = dict()

    if request.method == 'POST':
        data = dict(request.form)

        if 'reset' in data:
            redirect(url_for('index'))
            return render_template('index.html', sudokudata=sudoku_data)

        values = [val[0] for key, val in sorted(data.items())]
        values = ['0' if val == '' else val for val in values]
        values = ''.join(values)

        solution, solvable, next_digit = sudoku_solver.run(values)

        if 'clue' in data:
            sudoku_data = dict()
            for k in data.keys():
                sudoku_data[k] = data[k][0]

            if data['clue'] == 'digit':
                next_data = next_digit.values[0]
            elif data['clue'] == 'position':
                next_data = next_digit.keys[0]

            redirect(url_for('index'))
            return render_template('index.html', sudokudata=sudoku_data, next_data=next_data)

        if solvable:
            sudoku_data = solution
        else:
            sudoku_data = dict()
            for k in data.keys():
                sudoku_data[k] = data[k][0]

    redirect(url_for('index'))
    return render_template('index.html', sudokudata=sudoku_data)


if __name__ == '__main__':
    # app.debug = True
    app.run()
