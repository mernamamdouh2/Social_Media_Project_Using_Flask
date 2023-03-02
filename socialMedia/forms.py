from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from socialMedia.models import User, Post
from datetime import date

class RegistrationForm(FlaskForm):
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Length(min=3, max=20)
		]
	)
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email()
		]
	)
	password = PasswordField(
		'Password',
		validators=[
			DataRequired()
		]
	)
	confirm_password = PasswordField(
		'Confirm Password',
		validators=[
			DataRequired(),
			EqualTo('password')
		]
	)
	submit = SubmitField(
		'Sign Up'
	)


	#custom validation for duplicates
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exists')


class LoginForm(FlaskForm):
	username  = StringField(
		'Username',
		validators=[
			DataRequired(),
			Length(min=3, max=20)
		]
	)
	password = PasswordField(
		'Password',
		validators=[
			DataRequired()
		]
	)
	submit = SubmitField(
		'Sign In'
	)
 
 
class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
                    DataRequired(),
                    Length(min=3, max=20)
                   ]
    )
    content = StringField(
        'Content',
        validators=[
                    DataRequired(),
                    Length(min=3, max=20)
                   ]
    )
    privacy = SelectField(
		'Privacy',
        validators=[
                    DataRequired(),
                   ],
        choices=[('1','Public'),('2','Friends Only'),('3','Only Me')]
	)
    submit = SubmitField(
        'Post',
    ) 
    
class FriendsOnlyMode(FlaskForm):
    friends_only_mode = BooleanField(
        'friends only mode',
        validators=[
                    DataRequired(),
                   ]
    )
    submit = SubmitField(
        'Friends Only',
    )    
    
    
    
class UpdateForm(FlaskForm):
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Length(min=3, max=20)
		]
	)
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email()
		]
	)
	oldPassword = PasswordField(
		'Old Password',
		validators=[
			DataRequired()
		]
	)
	password = PasswordField(
		'Password',
	)
	confirm_password = PasswordField(
		'Confirm Password',
		validators=[
			EqualTo('password')
		]
	)
	submit = SubmitField(
		'Update'
	)    