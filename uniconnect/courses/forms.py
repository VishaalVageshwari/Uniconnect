from django import forms
from django.forms.widgets import TextInput, Textarea, NumberInput, HiddenInput
from django.core.validators import MinValueValidator, MaxValueValidator

from courses.models import Review

class ReviewForm(forms.ModelForm):
	feedback = forms.CharField(max_length=300,widget=Textarea({'class':'form-control', 'placeholder':'Maximum 300 characters','style': 'height: 10em;'}))
	rating = forms.IntegerField(
		widget= NumberInput({'max':5,'min':1}),
		validators=[
		MaxValueValidator(5),
		MinValueValidator(1)]
		)
	class Meta:
		model = Review
		fields = ['feedback','rating']
	
		