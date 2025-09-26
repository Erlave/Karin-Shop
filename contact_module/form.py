from django import forms

class ContactForm(forms.Form):
    phone = forms.CharField(max_length=15, required=True)
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
