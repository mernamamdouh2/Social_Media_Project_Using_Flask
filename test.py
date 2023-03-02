# os.environ['SECRET_KEY']
from socialMedia import db,app
import sys
from socialMedia.models import User
from socialMedia.models import Post

# create database
def create_db():
	with app.app_context():
		# you will have instance folder with site.db inside
		db.create_all()

# -------------------------- CRUD OPERATIONS --------------------------
# Create operation
def create_user():
	with app.app_context():
		user = User(name='merna',username='mernamamdouh2', email='mernamamdouh2@gmail.com', password='123')
		user2 = User(name='mamdouh',username='mamdouhmounir', email='mamdouhmounir@gmail.com', password='456')
		db.session.add(user)
		db.session.commit()
  
# Read operation
def read_user():
	with app.app_context():
		user = User.query.first()
		print(f"user is {user.username}")
		for post in user.posts:
			print(f"post : {post.name}")   

# Join queries
def read_join():
	with app.app_context():
		query = db.session.query(
			Post,
			User
			)\
			.join(User, Post.user_id == User.id)\
			.filter(User.email == "mernamamdouh2@gmail.com")\
			.order_by(Post.id.asc())\
			.all()

		for record in query:
			print(f"id : {record.Post.id}")
			print(f"name : {record.Post.name}")
			print(f"content : {record.Post.content}")
			print(f"User email : {record.User.email}\n")
        
# Update operation
def update_user():
	with app.app_context():
		user = User.query.filter_by(username="mamdouhmounir").first()
		user.password = '$2b$12$R3LWqFUKzawaWKaPNPp1wetUF.pp67lcnYhXQD6nW8EmqMivh44WK'
		db.session.commit()
    
# Delete operation
def delete_user():
    with app.app_context():
        user = User.query.filter_by(name='mamdouh').first()
        usr = User.query.all()
        db.session.delete(usr)
        db.session.commit()
        
             
# Create operation
def create_post():
	with app.app_context():
		user1 = User.query.first()
		user2 = User.query.offset(1).limit(1).first()
		# post1 = Post(title='HTML', text='html', date=60, user_id=user1.id)
		# post2 = Post(title='CSS', text='css', date=40, user_id=user2.id)
		post1 = Post(title='JAVA SCRIPT', text='java script', date=120, user_id=user1.id)
		post2 = Post(title='BOOTSTRAP', text='bootstrap', date=30, user_id=user2.id)
		db.session.add(post1)
		db.session.add(post2)
		db.session.commit()

# Read operation
def read_user_post():
    with app.app_context():
        user = User.query.first()
        print(user.posts)
        
# Read operation       
def read_post():
    with app.app_context():
        post = User.query.first()
        print(post)
        print(post.user_id)
        
# Delete operation
def delete_post():
    with app.app_context():
        #post = post.query.filter_by(name='HTML').first()
        pst = User.query.filter_by(name='mamdouh').first()
        db.session.delete(pst)
        db.session.commit()
        
        
# snippet to allow us to run funcs from terminal with "python test.py print_func"
if __name__ == '__main__':
	globals()[sys.argv[1]]()