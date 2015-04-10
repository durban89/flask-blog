#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
from contextlib import closing

#Configuration
DATABASE='/tmp/app.db'
LOGGER_FILE='/tmp/logger.log'
DEBUG=True
SECRET_KEY="z\xe5v\xf1'\xde\x99\xa3P|\xa8 \xe1\xd25op\xdd\xe96\r\xd3\xb7o"
USERNAME='admin'
PASSWORD='default'
ADMINS= ['zhangdapeng89@126.com']


app = Flask(__name__)
app.config.from_object(__name__)

#=======================数据库配置=========================#
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource("schema.sql",mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()
        
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()
    
@app.teardown_request
def teardown_request(exception):
    db = getattr(g,'db',None)
    if db is None:
        db.close()
    g.db.close()
    
#=======================邮件日志=========================#
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    from logging import Formatter
    mail_handler = SMTPHandler('127.0.0.1',
                               'zhangdapeng89@126.com',
                               ADMINS,
                               'Your Application Error!')
    mail_handler.setFormatter(Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

#=======================日志文件=========================#
if not app.debug:
    import logging
    from logging.handlers import WatchedFileHandler
    from logging import Formatter
    file_handler = WatchedFileHandler(app.config['LOGGER_FILE'])
    file_handler.setFormatter(Formatter('''
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
    '''))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

#=======================订阅信号=========================#
from flask import template_rendered
from contextlib import contextmanager

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender,template,context,**extra):
        recorded.append((template,context))

    template_rendered.connect(record,app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record,app)





#=======================视图程序逻辑=========================#
import flask_blog.views
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3031,debug=True)