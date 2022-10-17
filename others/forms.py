from django import forms
from django import forms
from . models import Message

class MessageForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name *', 'type':'name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email *', 'type':'email'}))
    body = forms.CharField(widget=forms.Textarea( attrs={'class':'form-control n-text' }))

    class Meta:
        model = Message
        exclude = ['addressed', 'timestamp']