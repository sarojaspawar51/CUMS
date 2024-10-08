from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
	def create_user(self,email, password,firstname=None,lastname=None, **extra_fields):
		if not email:

			raise ValueError("email is must")
		email=self.normalize_email(email)
		user=self.model(email=email,password=password,firstname=firstname, lastname=lastname,**extra_fields)
		user.set_password(password)
		user.save()
		

	def create_superuser(self,email,password,firstname=None, lastname=None,**extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)
		extra_fields.setdefault("is_active", True)
		if extra_fields.get('is_staff')is not True:
			raise ValueError('super user must have staff user!')
		if extra_fields.get('is_superuser')is not True:
			raise ValueError('super user must have is super user!')
		
		return self.create_user(email,password,firstname,lastname, **extra_fields)