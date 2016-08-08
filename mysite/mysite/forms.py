from django import forms

class ContactForm(forms.Form):
    full_name   =   forms.CharField()
    subject =   forms.CharField()
    message =   forms.CharField()
    email   =   forms.EmailField(required=False)
