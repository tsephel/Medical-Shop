from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(
			self, first_name, last_name, username, email, password=None):
		"""
		Creates and saves a User with the given email, full name
		and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		if not username:
			raise ValueError('Users must have a username')
       

		user = self.model(
			email=self.normalize_email(email), #normalize turns to small letter evne if we type capital 
			username = username,
			first_name=first_name, 
			last_name=last_name,          
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	#sets what kind of information is needed while created superuser(admin)
	def create_superuser(self, first_name, last_name, username, email, password):
		"""
		Creates and saves a superuser with the given email, first name,
		last name and password.
		"""
		user = self.create_user(
			email=self.normalize_email(email),
			username = username,
			password = password,
			first_name=first_name,
			last_name = last_name

		)
		user.is_admin = True
		user.is_active = True
		user.is_staff = True
		user.is_superadmin = True
		user.save(using=self._db)
		return user


# Created a new class called CustomUser that subclasses AbstractUser
# Added fields for email, is_staff, is_active, and date_joined
# Set the USERNAME_FIELD -- which defines the unique identifier for the User model -- to email
# Specified that all objects for the class come from the CustomUserManager
class Account(AbstractBaseUser):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	username = models.CharField(max_length=100, unique=True)
	email = models.EmailField(max_length=100, unique=True)
	phone_number = models.CharField(max_length=50)

	#required fields when creating custome user model
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	is_superadmin = models.BooleanField(default=False)

	#to make the user login with email address
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	objects = MyAccountManager()

	#means when we return account oject we return email address
	def __str__(self):
		return self.email

	#if user is admin than it has permission to do stuff
	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return self.is_admin

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True
