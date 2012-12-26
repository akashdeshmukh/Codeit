from django import forms


class UserForm(forms.Form):
    receipt_no = forms.IntegerField()
    first_name = forms.CharField()
    last_name = forms.CharField()


class FileUploadForm(forms.Form):
    code = forms.FileField(
        label='Select a file',
        help_text='max. 42 bytes'
        )
    CHOICES = (('a', 'c'),
               ('b', 'c++'),
               ('c', 'java'),
               ('d', 'python'),)
    picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())
