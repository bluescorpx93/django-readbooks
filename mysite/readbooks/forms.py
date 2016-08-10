from django import forms
from models import *

class AddAuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = ['first_name', 'last_name', 'bio', 'date_of_birth', 'gender', 'profile_picture' ]

class AddReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['heading', 'status','book', 'review',]

class UserPassChangeForm(forms.Form):
	currentPass = forms.CharField(widget=forms.PasswordInput)
	newPass1 = forms.CharField(widget=forms.PasswordInput)
	newPass2 = forms.CharField(widget=forms.PasswordInput)
	# class Meta:
	# 	model=models.User
	# 	fields = ['password']