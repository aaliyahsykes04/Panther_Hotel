from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'hotel.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn =get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        name TEXT NOT NULL,
        checkin_date TEXT NOT NULL,
        checkout_date TEXT NOT NULL, 
        room_type TEXT NOT NUll 
        )
    ''')
    conn.commit()
    conn.close()

    @app.route('/')
    def welcome():
        return render_template('welcome.html')

    @app.route('/reserve', methods=['GET','POST'])
    def reserve():
        if request.method == 'POST':
            name = request.form['name']
            checkin = request.form['checkin_date']
            checkout = request.form['checkout_date']
            room_type = request.form['room_type']
            conn =get_db()
            conn.execute(
                'INSERT INTO reservations (name, checkin_date, checkout_date, room_type) VALUES (?,?,?,?)',
                (name, checkin, checkout,room_type)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('confirmation' , name=name, checkin=checkin, checkout=checkout, room_type=room_type))
        return render_template('reservation.html')

    @app.route('/confirmation')
    def confirmation():
        name = request.args.get('name')
        checkin = request.args.get('checkin')
        checkout = request.args.get('checkout')
        room_type = request.args.get('room_type')
        return render_template('confirmation.html', name=name, checkin=checkin, checkout=checkout,room_type=room_type)

    @app.route('/manager')
    def manager():
        conn = get_db()
        reservations = conn.execute('SELECT * FROM reservations').fetchall()
        conn.close()
        return render_template('manager.html', reservations=reservations)

    if __name__ == '__main__':
        init_db()
        app.run(debug=True)