from django import forms
from models import *

# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = models.User
#         fields = []

class UserProfileForm(forms.Form):
	first_name = forms.CharField()
	last_name = forms.CharField()
	bio = forms.CharField(max_length=500)
	gender_choices	= 	(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
	gender = forms.ChoiceField(label="gender", choices=gender_choices)
	date_of_birth = forms.DateField()
	profile_picture = forms.ImageField()
        # fields = ['gender', 'bio', 'profile_picture', 'date_of_birth' ]

class AddBookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'author', 'publisher', 'genre', 'publication_date', 'cover_picture', 'book_synopsis']
		# widgets = {	'title': forms.TextInput(attrs={'placeholder': 'Title of the book', 'class':'form-control','id': 'booktitle', 'id':'title'}), 'author': forms.Select(attrs={'class': 'form-control', 'id':'author'}), 'publisher': forms.Select(attrs={'class': 'form-control',}), 'genre': forms.SelectMultiple(attrs={'class': 'form-control',}), 'publication_date' : forms.DateInput(attrs={'class': 'form-control',}), 'cover_picture': forms.FileInput(),			'book_synopsis': forms.Textarea(attrs={'class': 'form-control','placeholder': "What's the story about?"}), }


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