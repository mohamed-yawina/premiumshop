from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Nom complet", max_length=100)
    email = forms.EmailField(label="Adresse email")
    subject = forms.CharField(label="Sujet", max_length=150)
    message = forms.CharField(label="Message", widget=forms.Textarea)
