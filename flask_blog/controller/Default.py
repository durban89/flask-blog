#-*- coding=utf-8 -*-
__author__ = 'davidzhang'

from flask_blog import app
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash

def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)
login.provide_automatic_options = False
login.methods = ['POST','GET','OPTIONS']

def logout():
    session.pop('logged_in',None)
    flash('You are logged out')
    return redirect(url_for('show_entries'))
logout.provide_automatic_options = False
logout.methods = ['POST','GET','OPTIONS']
