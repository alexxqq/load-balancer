from django import forms

class YourForm(forms.Form):
    address_choices = [[f'127.0.0.1:500{i}' for i in range(1,10)]]
    
    address = forms.ChoiceField(choices=address_choices)
