import sqlite3
from flask import Flask, flash
from werkzeug.exceptions import abort

# Conn initializer
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATE Functions -----------------------------------------------------------------------------
def create_new_transaction(payer, points):
    conn = get_db_connection()
    conn.execute('INSERT INTO transactions (payer, points) VALUES (?, ?)',
         (payer, points,))
    conn.commit()
    conn.close()

# READ Functions --------------------------------------------------------------------------------
def read_payers():
    conn = get_db_connection()
    table = conn.execute("SELECT payer, SUM(points) AS total_points FROM transactions GROUP BY payer").fetchall()
    conn.close()
    return table

def read_payer_points(payer): # this is used in creating a transaction to ensure payer has enough points for transaction.
    conn = get_db_connection()
    table = conn.execute("SELECT SUM(points) as sum_of_points FROM transactions WHERE payer=?",
        (payer,)).fetchone()
    conn.close()
    return table

def read_highest_id():
    conn = get_db_connection()
    table = conn.execute("SELECT MAX(id) as recent_transaction FROM transactions").fetchone()
    conn.close()
    return table

def read_transaction_from_id(id):
    conn = get_db_connection()
    table = conn.execute("SELECT payer, points FROM transactions WHERE id=?", (id,)).fetchone()
    conn.close()
    return table

def read_all_transactions_ordered_by_timestamp():
    conn = get_db_connection()
    table = conn.execute("SELECT * FROM transactions ORDER BY timestamp_ DESC").fetchall()
    conn.close()
    return table

def read_total_points():
    conn = get_db_connection()
    table = conn.execute("SELECT SUM(points) as total_points FROM transactions").fetchone()
    conn.close()
    return table

# UPDATE Functions ---------------------------------------------------------------------------

def update_spend_points(points):
    conn = get_db_connection()

    conn.execute('INSERT INTO transactions ?,?',
         (points,))

    conn.commit()
    conn.close()



# DELETE Functions ---------------------------------------------------------------------------------------
def delete_transaction(id): # Never used cause not requested in document.
    conn = get_db_connection()
    conn.execute('DELETE FROM transactions WHERE id=?',
        (id,))
    conn.commit()
    conn.close()