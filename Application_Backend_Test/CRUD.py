import sqlite3
from flask import Flask, flash
from werkzeug.exceptions import abort

# Conn initializer
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATE Functions -----------------------------------------------------------------------------
def create_new_payer(payer, points):
    conn = get_db_connection()
    conn.execute('INSERT INTO userData (payer, points) VALUES (?, ?)',
         (payer, points))
    conn.commit()
    conn.close()

# READ Functions --------------------------------------------------------------------------------
def read_all():
    conn = get_db_connection()
    table = conn.execute("SELECT * FROM userData").fetchall()
    conn.close()
    return table

def read_payer_list():
    conn = get_db_connection()
    payer_list = []
    for row in conn.execute("SELECT payer FROM userData").fetchall():
        payer_list.append(row['payer'])
    conn.close()
    return payer_list

def read_all_ordered_by_timestamp():
    conn = get_db_connection()
    table = conn.execute("SELECT * FROM userData ORDER BY timestamp_ DESC").fetchall()
    conn.close()
    return table


def read_payer(payer):
    conn = get_db_connection()
    table = conn.execute("SELECT * FROM userData WHERE payer = ?", (payer,)).fetchone()
    conn.close()
    if payer is None :
        abort(404)
    return table

def read_total_points_of_payers():
    conn = get_db_connection()
    total_points = conn.execute("SELECT SUM(points) AS total_points FROM userData").fetchone()
    conn.close()
    return total_points



# UPDATE Functions ---------------------------------------------------------------------------
# Add points to payer, remove points, remove points from multiple users
def update_add_points_to_payer(payer, points):
    _payer_data = read_payer(payer)
    _payer = _payer_data['payer']
    _points = int(_payer_data['points']) + points
    conn = get_db_connection()
    conn.execute('UPDATE userData SET points=? WHERE payer=?',
         (_points,_payer))
    conn.execute('UPDATE userData SET timestamp_ = CURRENT_TIMESTAMP WHERE payer=?',
         (_payer,))
    conn.commit()
    conn.close()

def update_remove_points_from_payer(payer, points):
    _payer_data = read_payer(payer)
    _payer = _payer_data['payer']
    _points = int(_payer_data['points']) - points
    conn = get_db_connection()
    conn.execute('UPDATE userData SET points=? WHERE payer=?',
         (_points,_payer))
    conn.execute('UPDATE userData SET timestamp_ = CURRENT_TIMESTAMP WHERE payer=?',
         (_payer,))
    conn.commit()
    conn.close()

def update_remove_points_from_payers_based_on_timestamps(remove_points):
    _payers_data = read_all_ordered_by_timestamp()
    for _payer_data in _payers_data:
        if (remove_points > 0):
            _payer = _payer_data['payer']
            _points = _payer_data['points']
            if (remove_points >= _points):
                update_remove_points_from_payer(_payer, _points)
                remove_points-= _points
            else:
                update_remove_points_from_payer(_payer,  remove_points)
                remove_points-= remove_points
        else:
            break

# DELETE Functions ---------------------------------------------------------------------------------------
def delete_payer(payer):
    conn = get_db_connection()
    conn.execute('DELETE FROM userData WHERE payer=?',
        (payer,))
    conn.commit()
    conn.close()