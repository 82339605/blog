#数据库的操作，都放在这里
from . import db
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    cate_name = db.Column(db.String(50),nullable=False)
    topics = db.relationship('Topic',backref = 'category',lazy = 'dynamic')
class BlogType(db.Model):
    __tablename__ = 'blogtype'
    id = db.Column(db.Integer,primary_key=True)
    type_name = db.Column(db.String(20),nullable=False)
    topics = db.relationship('Topic',backref = 'blogType',lazy = 'dynamic')
    def change(self):
        dic = {
            'id':self.id,
            'type_name':self.type_name,
        }
        return dic
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    loginname = db.Column(
    db.String(50),nullable=False)
    uname = db.Column(db.String(30),nullable=False)
    email = db.Column(
    db.String(200),nullable=False)
    url = db.Column(db.String(200))
    upwd=db.Column(db.String(30),nullable=False)
    is_author=db.Column(db.SmallInteger,default=0)
    topics = db.relationship('Topic',lazy = 'dynamic',backref = 'user')
    replies = db.relationship('Reply', backref='user', lazy="dynamic")
    voke_topics = db.relationship(
        'Topic',
        secondary='voke',
        backref=db.backref('voke_users', lazy='dynamic'),
        lazy='dynamic'
    )
    def __init__(self,loginname,uname,email,url,upwd):
        self.loginname=loginname
        self.uname=uname
        self.email=email
        self.url=url
        self.upwd=upwd
class Topic(db.Model):
      __tablename__ = "topic"
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(
          db.String(200), nullable=False)
      pub_date = db.Column(
          db.DateTime, nullable=False)
      read_num = db.Column(db.Integer, default=0)
      content = db.Column(db.Text, nullable=False)
      images = db.Column(db.Text)
      category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
      blogtype_id = db.Column(db.Integer,db.ForeignKey('blogtype.id'))
      user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
      replies = db.relationship('Reply',backref = 'topic',lazy = 'dynamic')
      def __init__(self,title,content,category_id,blogtype_id,user_id,pub_date):
          self.title = title
          self.content=content
          self.category_id=category_id
          self.blogtype_id=blogtype_id
          self.user_id=user_id
          self.pub_date=pub_date
class Reply(db.Model):
      __tablename__ = 'reply'
      id = db.Column(db.Integer,primary_key=True)
      content = db.Column(db.Text,nullable=False)
      reply_time = db.Column(db.DateTime)
      user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
      topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'))
Voke = db.Table(
    'voke',
    db.Column('id',db.Integer,primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('topic_id',db.Integer,db.ForeignKey('topic.id'))
)
