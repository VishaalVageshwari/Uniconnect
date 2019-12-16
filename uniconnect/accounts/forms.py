from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput, Textarea, HiddenInput, FileInput

from accounts.models import Profile, Interest

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Password'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    first_name = forms.CharField(max_length=30, required=True, widget=TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(max_length=254, required=True,
    widget=TextInput(attrs={'class':'form-control', 'type':'email', 'placeholder':'Email'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        if commit:
            user.save()
            
        return user

class EditProfileForm(forms.ModelForm):
	user_id = forms.CharField(max_length=50, required=False, widget=HiddenInput())
	degree = forms.CharField(max_length=50, required=False, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Degree'}))
	biography = forms.CharField(max_length=300, required=False, widget=Textarea(attrs={'class':'form-control', 'placeholder':'Maximum 300 characters','style': 'height: 10em;'}))
	image = forms.ImageField(required=False, widget=FileInput(attrs={'class':'form-control', 'placeholder':'No file selected'}))

	class Meta:
		model = Profile
		fields = ('user_id','degree', 'biography', 'image')

class EditInterestsForm(forms.ModelForm):
	user_id = forms.CharField(max_length=50, required=False, widget=HiddenInput())
	interest = forms.CharField(max_length=30, required=False, widget=TextInput(attrs={'class':'form-control', 'placeholder':'Interest'}))
	class Meta:
		model = Interest
		fields = ('user_id','interest')
