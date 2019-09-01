from flask import url_for, flash, redirect, session
from functools import wraps

def login_required(func):
    @wraps(func)
    def check_session():
        if session.get('username') is None:
            flash(f'You need to log in first', 'warning')
            return redirect(url_for('login'))
        return func()
    return check_session

def logout_required(func):
    @wraps(func)
    def check_logout():
        if session.get('username'):
            flash(f'You are already logged in', 'success')
            return redirect(url_for('index'))
        return func()
    return check_logout
