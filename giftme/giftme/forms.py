from django import forms 

class GiftForm(forms.Form):
    text = forms.CharField(max_length=40, 
        widget=forms.TextInput(
            attrs={'class' : 'form-control', 'placeholder' : 'Enter Possible Gift', 'aria-label' : 'Gift', 'aria-describedby' : 'add-btn'}))