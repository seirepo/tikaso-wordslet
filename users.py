import secrets

from flask import session
from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user[0]
            session["user_role"] = user[2]
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def user_exists(username):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (username, password, role)
                VALUES (:username, :password, :role)"""
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False;
    return login(username, password)

def logout():
    del session["username"]
    del session["user_id"]
    del session["user_role"]

def get_username(id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    return user.username

def current_user():
    return session.get("username", 0)

def current_user_id():
    return session.get("user_id", 0)

def get_all_users():
    result = db.session.execute("SELECT id, username, role FROM users")
    users = result.fetchall()
    return users

def search_from_users(query):
    sql = """SELECT id, username FROM users WHERE username LIKE :query"""
    result = db.session.execute(sql, {"query":"%"+query+"%"}).fetchall()
    return result
