__author__ = 'davidzhang'
# -*- utf-8 -*-

from flask import Flask,request,g,session

def index():
    username = request.get_data('username')
    return "User %s" % username
index.provide_automatic_options =False
index.methods = ['GET','POST','OPTIONS']