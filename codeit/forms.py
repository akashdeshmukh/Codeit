from django import forms


class UserForm(forms.Form):
    receipt_no = forms.IntegerField()
    first_name = forms.CharField()
    last_name = forms.CharField()


class FileUploadForm(forms.Form):
    code = forms.FileField(
        label='Select a file',
        )
    CHOICES = (('c', 'C'),
               ('cpp', 'C++'),
               ('java', 'Java'),
               ('py', 'Python'),)
    picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())
