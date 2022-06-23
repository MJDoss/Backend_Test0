import sqlite3
import CRUD
from flask import Flask, redirect, url_for, request, render_template, flash
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Its a secret to everyone.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_transaction', methods = ['GET', 'POST'])
def create_transaction():
    if (request.method == 'POST'):
        _payer = request.form['payer']
        _points = int(request.form['points'])

        # if the points are negative we need to see if that payer has enough
        _payer_check = CRUD.read_payer_points(_payer)

        if not _payer: 
            flash('Payer name is required')
        elif not _points:
            flash('Starting points is required')
        elif (not isinstance(_points, int)):
            flash('Starting points is an integer') 
        elif(_payer_check['sum_of_points'] is None and _points > 0):
            CRUD.create_new_transaction(_payer, _points)
            flash('New transaction added to DB')
            return redirect(url_for('read_transactions'))
        elif (_payer_check['sum_of_points'] + _points < 0):
            flash('Payer lacks enough points')
        else:
            CRUD.create_new_transaction(_payer, _points)
            flash('New transaction added to DB')
            return redirect(url_for('read_transactions'))
    return render_template('create_transaction.html')


@app.route('/spend_points', methods = ['GET','POST'])
def spend_points():
    transaction_table = CRUD.read_all_transactions_ordered_by_timestamp()
    total_points = CRUD.read_total_points()
    if (request.method == 'POST'):
        _points = int(request.form['points'])
        # first check if there's enough points.
        if (_points > total_points['total_points']):
            flash('More points than available')
        elif (_points < 0):
            flash('Spending points must be a positive integer')
        else:
        # Build a dict with the payer as key and value as how many points the transaction is gonna be,
        # by going through the previous transactions list from most recent to oldest using the id column.
            _transactions = {}
            _highest_id = CRUD.read_highest_id()
            _id = _highest_id['recent_transaction']
            while (_points > 0):
                _cur_transaction = CRUD.read_transaction_from_id(_id)
                _cur_payer = _cur_transaction['payer']
                _cur_points = int(_cur_transaction['points'])
                if(_cur_points < _points):
                    if( _transactions.get(_cur_payer) is None):
                        _transactions.update({ _cur_payer : -_cur_points })
                    else :
                        _transactions.update({ _cur_payer : _transactions.get(_cur_payer) - _cur_points })
                    _points -= _cur_points
                else:
                    if( _transactions.get(_cur_payer) is None):
                        _transactions.update({ _cur_payer : -_points })
                    else :
                        _transactions.update({ _cur_payer : _transactions.get(_cur_payer) - _points })
                    _points -= _points
                _id-=1
            # Then re-use the create_transaction(payer,points) in a for loop with the transactions dict to pay it off
            for _t in _transactions.keys():
                _cur_payer = _t
                _cur_points = _transactions.get(_t)
                CRUD.create_new_transaction(_cur_payer, _cur_points)
            flash('New transactions added to DB')
            return redirect(url_for('read_transactions'))   
    return render_template('spend_points.html', transaction_table=transaction_table, total_points=total_points)

@app.route('/read_transactions', methods = ['GET'])
def read_transactions():
    transaction_table = CRUD.read_all_transactions_ordered_by_timestamp()
    return render_template('read_transactions.html', transaction_table=transaction_table)

@app.route('/read_payers', methods = ['GET'])
def read_payers():
    payer_table = CRUD.read_payers()
    return render_template('read_payers.html', payer_table=payer_table)


if __name__ == '__main__':
    app.run()