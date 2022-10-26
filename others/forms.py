from django import forms
from . models import Message

class MessageForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name*'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email*'}))
    body = forms.CharField(label='', widget=forms.Textarea( attrs={'class':'form-control', 'cols':'30', 'rows':'10', 'placeholder': 'Message*'}))

    class Meta:
        model = Message
        exclude = ['addressed', 'timestamp']