#主业务中视图和路由的定义
import datetime

from flask import render_template, request, session, redirect, json
import os

from . import main#导入蓝图，用于构建路由
from .. import db
from ..models import *
@main.route('/check')
def servertolove():
    name = request.args.get('username')
    data = User.query.filter_by(uname=name).first()
    if data:
        return '用户名已存在'
    return 'ok'
@main.route('/create',methods=["POST"])
def createname():
    loginname = request.form['loginname']
    username = request.form['username']
    email = request.form['email']
    url = request.form['url']
    upwd = request.form['password']
    user = User(loginname,username,email,url,upwd)
    db.session.add(user)
    db.session.commit()
    session['uid'] = user.id
    session['uname'] = user.uname
    return redirect('/')
@main.route('/register')
def findregister():
    return render_template('register.html')
@main.route('/logout')
def logout():
    if 'uid' in session and 'uname' in session:
        del session['uid']
        del session['uname']
    return redirect('/')
@main.route('/')
def main_index():
    information = Category.query.all()
    topics = Topic.query.all()
    if 'uid' in session and 'uname' in session:
        user = User.query.filter_by(id=session['uid']).first()
    return render_template('index.html',params = locals())
@main.route('/login',methods = ["POST","GET"])
def login():
    if 'uid' in session and 'uname' in session:
        return redirect('/')
    if request.method == "GET":
        return render_template('login.html')
    else:
        uname = request.form['username']
        pwd = request.form['password']
        user = User.query.filter_by(loginname=uname,upwd=pwd).first()
        if user:
            session['uid'] = user.id
            session['uname'] = user.uname
            return redirect('/')
        errmsg = '用户名或密码不正确'
        return render_template('login.html',errmsg=errmsg)
@main.route('/register')
def register():
    return render_template('register.html')
@main.route('/release',methods=['GET',"POST"])
def release():
    if request.method == "GET":
        if 'uid' in session and 'uname' in session:
            user = User.query.filter_by(id=session['uid']).first()
            if user.is_author==1:
                category = Category.query.all()
                blog = BlogType.query.all()
                return render_template('release.html',params=locals())
        return redirect('/')
    else:
        author = request.form['author']
        content = request.form['content']
        blog = request.form['list']
        category = request.form['category']
        topic = Topic(author,content,category,blog,session['uid'],datetime.datetime.now().strftime('%Y-%m-%d'))
        if request.files.get('file'):
            file = request.files.get('file')
            time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            exc = file.filename.split('.')[1]
            filename = time+'.'+exc
            path = os.path.dirname(__file__)
            fpath = os.path.join(path,'..','static/images',filename)
            file.save(fpath)
            topic.images = 'images/' + filename
        db.session.add(topic)
        return redirect(request.headers['referer'])
@main.route('/find')
def tofind():
    information = User.query.filter_by(id=1).first()
    for i in information.topics.all():
        print(i.title+":"+i.blogType.type_name)
    return 'ok'
@main.route('/info',methods = ["GET","POST"])
def info_views():
    if request.method == "GET":
        id = request.args['topic_id']
        topic = Topic.query.filter_by(id=id).first()
        topic.read_num = int(topic.read_num)+1
        db.session.add(topic)
        prev_topic = Topic.query.filter(Topic.id<topic.id).order_by('id desc').first()
        next_topic = Topic.query.filter(Topic.id>topic.id).first()
        if 'uid' in session and 'uname' in session:
            user = User.query.filter_by(id=session['uid'])
        return render_template('info.html',params = locals())
