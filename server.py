from flask import *
import os
import hashlib
import sqlite3
import json

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    password = request.form['password']
    login = request.form['login']

    connection = sqlite3.connect('network_database.db')
    cursor = connection.cursor()
    salt = cursor.execute(f'SELECT salt FROM users WHERE login =="{login}"').fetchone()[0]
    password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                   salt, 20000)
    if password == cursor.execute(f'SELECT password FROM users WHERE login =="{login}"').fetchone()[0]:
        connection.close()
        return 'Ok'
    else:
        connection.close()
        return 'No'


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    password = request.form['password']
    login = request.form['login']
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                              salt, 20000)
    connection = sqlite3.connect('network_database.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (login, password, salt)"
                   "VALUES (?, ?, ?)", (login, key, salt))
    connection.commit()
    connection.close()
    return 'Ok'


@app.route('/contacts', methods=['POST', 'GET'])
def contacts():
    name = request.form['name']
    connection = sqlite3.connect('network_database.db')
    cursor = connection.cursor()
    query = f"""
                SELECT login, image FROM users where _id in (SELECT cont.contact_id FROM contacts AS cont
                WHERE cont._id == (SELECT _id FROM users WHERE login =='{name}'))

    """
    contacts_list = cursor.execute(query).fetchall()
    return_dict = dict()
    j = 0
    for i in contacts_list:
        return_dict[str(j)] = i
        j += 1
    connection.close()
    return return_dict


@app.route('/add_contact', methods=['POST', 'GET'])
def add_contact():
    name = request.form['name']
    contact_name = request.form['contact_name']
    connection = sqlite3.connect('network_database.db')
    cursor = connection.cursor()
    cursor.execute(f"""INSERT INTO contacts(_id, contact_id)
    VALUES ((SELECT _id FROM users WHERE login =='{name}'), (SELECT _id FROM users WHERE login =='{contact_name}'))
    """)
    cursor.execute(f"""INSERT INTO contacts(contact_id, _id)
        VALUES ((SELECT _id FROM users WHERE login =='{name}'), (SELECT _id FROM users WHERE login =='{contact_name}'))
        """)
    connection.commit()
    return 'Ok'


if __name__ == '__main__':
    app.run(debug=True)
