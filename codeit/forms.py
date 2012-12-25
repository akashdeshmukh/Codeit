from django import forms


class UserForm(forms.Form):
    receipt_no = forms.IntegerField()
    first_name = forms.CharField()
    last_name = forms.CharField()
