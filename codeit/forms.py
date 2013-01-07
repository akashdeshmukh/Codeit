from django import forms


class UserForm(forms.Form):
    receipt_no = forms.IntegerField(label="Receipt No", widget=forms.TextInput(attrs={
      'placeholder': 'Receipt No'
      }))
    first_name = forms.CharField(label="First Name",  widget=forms.TextInput(attrs={
      'placeholder': 'First Name'
      }))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={
      'placeholder': 'Last Name'
      }))
    CHOICES = (
      ('fe', 'F.E.'),
      ('se', 'S.E.'),
      ('te', 'T.E'),
      ('be', 'B.E'),
      ('mca', 'M.C.A'),
      )
    year = forms.ChoiceField(choices=CHOICES)


class FileUploadForm(forms.Form):
    code = forms.FileField(
        label="Select code file to Upload",
        )
    CHOICES = (
      ("c", "C"),
      ("cpp", "C++"),
      ("java", "Java"),
      ("py", "Python"),
      )
    picked = forms.ChoiceField(choices=CHOICES, label="Select your language")
