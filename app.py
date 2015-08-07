#-*- coding: utf-8 -*-

import sqlite3
import os
from flask import *

app = Flask(__name__)

# 配置项
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)
app.config['DATABASE'] = os.path.join(app.root_path, 'database/LS.db')

# 数据库相关
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])
@app.before_request
def before_request():
	g.db = connect_db()
@app.teardown_request
def teardown_request(exception):
	g.db.close()
def query_db(query, args=(), one=False):
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value) 
		for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv

# 组件&函数


# 路由
@app.route("/")
def index():
	return render_template("index.html")

# 启动项
if __name__ == "__main__":
	app.run()