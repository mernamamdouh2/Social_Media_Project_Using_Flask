from socialMedia import * 
from flask import render_template, url_for, redirect, flash, Blueprint
from socialMedia.forms import RegistrationForm, LoginForm, PostForm, FriendsOnlyMode, UpdateForm
from socialMedia.models import User, Post, Friendship, Notifications
from flask import request
from test import create_db
from flask_login import login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# blueprint
users = Blueprint(
	'users',
	__name__,
	url_prefix='/users'
)


#Registration Page         
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registration Successful. You can now log in. {form.username.data}", "success"')
        with app.app_context():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
            new_user=User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
        flash(f"Registration Successful {form.username.data}", "success")
        return redirect(url_for('users.login'))
            
    return render_template('register.html', title='Registration Page', form=form)


#Login Page 
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():        
        user = User.query.filter_by(username=form.username.data).first()
        # if user exists , check his password
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash(f"Login Successful {user.username}", "success")
            return redirect(url_for('home'))
        else:
            flash(f"Incorrect username or password. Please try again.", "danger")
            return render_template('login.html', title='Login Page', form=form)
        
    return render_template('login.html', title='Login Page', form=form)

        
#Logout Page 
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


#Home Page  
@app.route('/') 
@app.route('/home', methods=["POST","GET"])
def home(): 
    if current_user.is_authenticated:
        all_myPosts = Post.query.filter_by(user_id=current_user.id).order_by(Post.post_date.desc()) 
       
        friends_id1 = Friendship.query.with_entities(Friendship.sender_id.label('id')).filter_by(receiver_id=current_user.id).filter(Friendship.accepted==True)
        friends_id2 = Friendship.query.with_entities(Friendship.receiver_id.label('id')).filter_by(sender_id=current_user.id).filter(Friendship.accepted==True)
        friends = []
        for friend in friends_id1:
            friends.append(friend.id)
        for friend in friends_id2:
            friends.append(friend.id) 
        
        meAndMyFriends = friends
        meAndMyFriends.append(current_user.id)    
        
        friends_posts = Post.query.filter(Post.user_id.in_(friends)).filter( Post.privacy.in_([1,2])).order_by(Post.post_date.desc()) 
        public_posts = Post.query.filter(Post.user_id.notin_(meAndMyFriends)).filter(Post.privacy==1).order_by(Post.post_date.desc()) 
        
        form = FriendsOnlyMode()
        if form.validate_on_submit():
            mode = request.form['friends_only_mode'] 
            if mode: 
                display_posts = set(all_myPosts).union(set(friends_posts)) 
            else: 
                display_posts = set(all_myPosts).union(set(public_posts)).union(set(friends_posts))
        else:
            display_posts = set(all_myPosts).union(set(public_posts)).union(set(friends_posts))
    
        return render_template('home.html', posts=display_posts, form=form,title='Home') 
    else:
       return render_template('home.html', posts=[], title='Home')  
  
  
#Profile Page    
@app.route('/profile') 
def profile():
    all_myPosts = Post.query.filter_by(user_id=current_user.id).order_by(Post.post_date.desc())
    
    return render_template('profile.html',title='Posts',posts=all_myPosts, form=PostForm()) 


#Update UserInfo Page         
@app.route('/update', methods=['GET', 'POST'])
def updateUserInfo():
    form = UpdateForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password,form.oldPassword.data):
            if form.password.data:
                user = User.query.filter_by(username=current_user.username).first()
                user.username = form.username.data
                user.email = form.email.data
                user.password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
                db.session.commit()
            else:
                user = User.query.filter_by(username=current_user.username).first()
                user.username = form.username.data
                user.email = form.email.data 
                db.session.commit()  
                
            return redirect(url_for('profile')) 
        else:
            flash(f"Incorrect password. Please try again.", "danger") 
    return render_template('updateform.html', title='Update Form Page', form=form ,userData=current_user)
   

#All Users Page
@app.route('/allUsers', methods= ['GET'])
def allUsers():
    friends_id1 = Friendship.query.with_entities(Friendship.sender_id.label('id')).filter_by(receiver_id=current_user.id).filter(Friendship.accepted==True)
    friends_id2 = Friendship.query.with_entities(Friendship.receiver_id.label('id')).filter_by(sender_id=current_user.id).filter(Friendship.accepted==True)
    friends = []
    for friend in friends_id1:
        friends.append(friend.id)
    for friend in friends_id2:
        friends.append(friend.id)    
    friends_requestRecieved = Friendship.query.with_entities(Friendship.sender_id.label('id')).filter_by(receiver_id=current_user.id).filter(Friendship.accepted==False)
    friends_requestSended = Friendship.query.with_entities(Friendship.receiver_id.label('id')).filter_by(sender_id=current_user.id).filter(Friendship.accepted==False)
    friendRequestSended = []
    friendRequestRecieved = []
    for friend in friends_requestSended:
        friendRequestSended.append(friend.id)
    for friend in friends_requestRecieved:
        friendRequestRecieved.append(friend.id)
    allUsers = User.query.filter(User.id!=current_user.id).all()
    
    return render_template('allUsers.html',friends=friends, allUsers=allUsers, friends_requestSended=friendRequestSended, friends_requestRecieved=friendRequestRecieved )
    

#Make Friend Request
@app.route('/makeFriendRequest/<int:friend_id>', methods= ['GET'])
def makeFriendRequest(friend_id):
    friendship = Friendship(sender_id=current_user.id, receiver_id=friend_id)
    db.session.add(friendship) 
    db.session.commit() 
    notification = Notifications(user_id=friend_id,message="you have a new friend request from " + current_user.username)
    db.session.add(notification) 
    db.session.commit() 
    flash('You send a friend request successfully!','success') 
    return redirect(url_for('profile')) 


#Friend Requests Page 
@app.route('/friend_requests') 
def friend_requests(): 
    requests = Friendship.query.with_entities(Friendship.sender_id).filter_by(receiver_id=current_user.id,accepted=0).all() 
    myRequests = []
    for req in requests:
        myRequests.append(req.sender_id)
        
    users = User.query.filter(User.id.in_(myRequests)).all() 
    
    return render_template('friend_requests.html',requests=users)


#Accept Friend Request 
@app.route('/accept_request/<friend_id>',methods=['GET']) 
def accept_request(friend_id): 
    request = Friendship.query.filter_by(sender_id=friend_id,receiver_id=current_user.id,accepted=0).first() 
    if request:   
        request.accepted = 1 
        db.session.add(request) 
        db.session.commit() 
        notification = Notifications(user_id=friend_id,message= current_user.username + " has accepted your request ..")
        db.session.add(notification) 
        db.session.commit() 
    return redirect(url_for('friend_requests')) 
 
 
#Reject Friend Request 
@app.route('/reject_request/<friend_id>',methods=['GET','POST']) 
def reject_request(friend_id): 
    request = Friendship.query.filter_by(sender_id=friend_id, receiver_id=current_user.id,accepted=0).first() 
    if request: 
        db.session.delete(request) 
        db.session.commit() 
        notification = Notifications(user_id=friend_id,message= current_user.username + " has refused your request ..")
        db.session.add(notification) 
        db.session.commit()
    return redirect(url_for('friend_requests'))


#Friends Page
@ app.route('/friends') 
def friends(): 
    friends_id1 = Friendship.query.filter_by(receiver_id=current_user.id).filter(Friendship.accepted==True)
    friends_id2 = Friendship.query.filter_by(sender_id=current_user.id).filter(Friendship.accepted==True)
    friends= set(friends_id1).union(set(friends_id2)) 
        
    return render_template('friends.html',friends=friends )

    
#Create New Post
@app.route('/create_post',methods=['POST']) 
def create_post(): 
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(user_id=current_user.id,title=request.form['title'],content=request.form['content'] ,privacy=request.form['privacy']) 
        db.session.add(new_post) 
        db.session.commit() 
        flash('Your post was created!','success') 
        return redirect(url_for('profile')) 
    else: 
        return redirect(url_for('profile')) 
    
#Update Post 
@app.route('/posts/update/<int:id>', methods=['GET','POST']) 
def update_post(id): 
    post = Post.query.filter_by(id=id).first() 
    print(post)
    if request.method == 'POST': 
        form = PostForm() 
        if form.validate_on_submit(): 
            post.title = form.title.data 
            post.content = form.content.data 
            post.privacy = form.privacy.data 
            db.session.commit() 
        return redirect(url_for('profile'))  
    else:
        return render_template('updatePost.html', form=PostForm(), post=post)
    
    
#Delete Post 
@app.route('/posts/delete/<int:id>', methods=['GET']) 
def delete(id): 
    post = Post.query.filter_by(id=id).first()          
    if post: 
        db.session.delete(post) 
        db.session.commit() 
    return redirect(url_for('profile')) 


#My Notification Page
@app.route('/myNotification', methods=['GET'])
def myNotification():
    notifications = Notifications.query.filter_by(user_id=current_user.id).all()
    return render_template('myNotification.html', notifications=notifications)  

  
#Seen Notifications or not    
@app.route('/seenNotification/<id>', methods=['GET'])        
def seenNotification(id):
    notification = Notifications.query.filter_by(id=id).first()
    notification.seen = 1 
    db.session.commit()
    return redirect(url_for('myNotification'))

