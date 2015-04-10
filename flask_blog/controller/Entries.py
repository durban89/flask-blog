#!/usr/bin/env python
#-*- coding=utf-8 -*-
__author__ = 'davidzhang'

from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash

def show_entries():
    cur = g.db.execute("select title,text from entries order by id DESC")
    entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html',entries=entries)
show_entries.provide_automatic_options = False
show_entries.methods = ['GET', 'OPTIONS']

def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute("insert into entries (title,text) values (?,?)",[request.form['title'],request.form['text']])
    g.db.commit()
    flash('New Entry was successfully posted')
    return redirect(url_for('show_entries'))
add_entry.provide_automatic_options = False
add_entry.methods = ['POST', 'OPTIONS']