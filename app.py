from flask import Flask, render_template, request, session, redirect, g, url_for, abort, flash, Markup, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from datetime import datetime
import os
from sqlalchemy.orm import sessionmaker
import time
import json
import numpy as np
from sudoku_solver import SudokuSolver

app = Flask(__name__)
#app.secret_key = os.urandom(12)
#app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#heroku = Heroku(app)
#db = SQLAlchemy(app)


sudoku_solver = SudokuSolver(solve=True)


# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html', ingrid='index') #, sudokudata='')


@app.route('/solve', methods=['POST'])
def solve():
    sudoku_data = dict()

    if request.method == 'POST':
        data = dict(request.form)

        values = [val[0] for key, val in sorted(data.items())]
        values = ['0' if val == '' else val for val in values]
        values = ''.join(values)

        solution, solved = sudoku_solver.run(values)

        if solved:
            sudoku_data = solution
        else:
            sudoku_data = data

    redirect(url_for('index'))
    return render_template('index.html', sudokudata=sudoku_data, ingrid='hej')


if __name__ == '__main__':
    # app.debug = True
    app.run()
