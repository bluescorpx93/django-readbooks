from django import forms
from readbooks import models

class AddAuthorForm(forms.ModelForm):
	class Meta:
		model = models.Author
		fields = ['profile_picture']

class AddReviewForm(forms.ModelForm):
	class Meta:
		model = models.Review
		fields = ['heading', 'status','book', 'review',]
