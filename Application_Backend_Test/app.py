import sqlite3
import CRUD
from flask import Flask, redirect, url_for, request, render_template, flash
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Its a secret to everyone.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_payer', methods = ['GET', 'POST'])
def create_payer():
    payers_table = CRUD.read_payer_list()
    error = None
    if (request.method == 'POST'):
        payer_name = request.form['payer']
        starting_points = int(request.form['points'])
        if not payer_name: 
            flash('Payer name is required')
        elif not starting_points:
            flash('Starting points is required')
        elif (not isinstance(starting_points, int)):
            flash('Starting points is an integer')
        elif (isinstance(starting_points, int)) and (starting_points < 0):
            flash('Starting points is a positive only integer') 
        elif payer_name in payers_table:
            flash('Invalid Credentials : payer name, already in use.')    
        else:
            CRUD.create_new_payer(payer_name, starting_points)
            flash('new Payer added to DB')
            return redirect(url_for('read_payers'))
    return render_template('create_payer.html', payers_table=payers_table, error=error)


@app.route('/read_payers', methods = ['GET'])
def read_payers():
    payers_table = CRUD.read_all()
    return render_template('read_payers.html', payers_table=payers_table)

@app.route('/add_points_to_a_payer', methods = ['GET', 'POST'])
def add_points_to_a_payer():
    payers_table = CRUD.read_all()
    _payers = CRUD.read_payer_list()
    error = None
    if (request.method == 'POST'):
        payer_name = request.form['payer']
        adding_points = int(request.form['points'])
        if not payer_name: 
            flash('Payer name is required')
        elif not adding_points:
            flash('Adding points is required')
        elif (adding_points < 0):
            flash('Adding points is a positive only integer')  
        elif (payer_name not in _payers):
            flash('Invalid Credentials : Payer name not found.')
        else:
            CRUD.update_add_points_to_payer(payer_name, adding_points)
            flash('Points added to payer!')
            return redirect(url_for('read_payers'))
    return render_template('add_points_to_a_payer.html', payers_table=payers_table, error=error)

@app.route('/remove_points_from_a_payer', methods = ['GET', 'POST'])
def remove_points_from_a_payer():
    payers_table = CRUD.read_all()
    _payers = CRUD.read_payer_list()
    error = None
    if (request.method == 'POST'):
        payer_name = request.form['payer']
        removing_points = int(request.form['points'])
        payer_data = CRUD.read_payer(payer_name)
        payer_points = payer_data['points']
        if not payer_name: 
            flash('Payer name is required')
        elif not removing_points:
            flash('spendinging points is required')
        elif (removing_points < 0):
            flash('Spending points is a positive only integer')  
        elif (payer_name not in _payers):
            flash('Invalid Credentials : Payer name not found.')
        elif (removing_points > payer_points):
            flash('Invalid Credentials : More points than payer has.')
        else:
            CRUD.update_remove_points_from_payer(payer_name, removing_points)
            flash('Payer spent points!')
            return redirect(url_for('read_payers'))
    return render_template('remove_points_from_a_payer.html', payers_table=payers_table, error=error)


@app.route('/remove_points_from_multiple_payers', methods = ['GET', 'POST'])
def remove_points_from_multiple_payers():
    payers_table = CRUD.read_all_ordered_by_timestamp()
    total_points = CRUD.read_total_points_of_payers()
    _total_points = total_points['total_points']
    error = None
    if (request.method == 'POST'):
        removing_points = int(request.form['points'])
        if not removing_points:
            flash('removing points is required')
        elif (removing_points < 0):
            flash('Spending points is a positive only integer')  
        elif (removing_points > _total_points):
            flash('Invalid Credentials : More points than total points of all payers.')
        else:
            CRUD.update_remove_points_from_payers_based_on_timestamps(removing_points)
            flash('The Payers their spent points!')
            return redirect(url_for('read_payers'))
    return render_template('remove_points_from_multiple_payers.html', payers_table=payers_table, error=error, total_points=total_points)


if __name__ == '__main__':
    app.run()