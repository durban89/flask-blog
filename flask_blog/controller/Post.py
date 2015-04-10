__author__ = 'davidzhang'
# -*- coding: UTF-8 -*-

from flask import Flask,request,render_template,url_for

def index():
    id = request.get_data('id')
    return "Post: %s" % id
index.provide_automatic_options = False
index.methods = ['GET','POST','OPTIONS']