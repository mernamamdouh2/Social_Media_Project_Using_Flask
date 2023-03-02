from socialMedia import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# Create User Model
class User(db.Model, UserMixin):
    """Model to define User"""
    __tablename__ = 'user' 
    
    id = db.Column(db.Integer,primary_key=True) 
    username = db.Column(db.String(50),nullable = False) 
    email = db.Column(db.String(50), unique=True,nullable = False)
    password = db.Column(db.String(100),nullable = False) 
    join_date = db.Column(db.DateTime, default = datetime.utcnow)
    

# Create Post Model      
class Post(db.Model):
    """Model to define Item"""
    __tablename__ = 'post' 
     
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    title = db.Column(db.String(120),nullable = False)
    content = db.Column(db.Text,nullable = False) 
    privacy = db.Column(db.String(30),nullable = False)
    post_date = db.Column(db.DateTime, default=datetime.now())
    

# Create Friendship model to store requests
class Friendship(db.Model):
    __tablename__ = "friendship"
    
    id = db.Column(db.Integer,primary_key = True)
    sender_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    receiver_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    accepted = db.Column(db.Boolean, default=False)
    
    
# Create Notification Model
class Notifications(db.Model):
    __tablename__ = "notifications"
    
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    message = db.Column(db.String(250),nullable = False) 
    seen = db.Column(db.Boolean,default=False)          