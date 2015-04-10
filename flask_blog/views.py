__author__ = 'davidzhang'
# -*- coding: UTF-8 -*-

from flask_blog import app

#导入控制器
from controller import Entries
from controller import Default
from controller import User
from controller import Post

#路由控制
app.add_url_rule('/','show_entries',Entries.show_entries)
app.add_url_rule('/add','add_entry',Entries.add_entry)
app.add_url_rule('/login/','login',Default.login)
app.add_url_rule('/login/','logout',Default.logout)
app.add_url_rule('/user/','user',User.index)
app.add_url_rule('/user/','post',Post.index,defaults={'page':'index'})
