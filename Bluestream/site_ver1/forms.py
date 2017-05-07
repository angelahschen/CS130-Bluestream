from django import forms
from .models import Person
class PersonForm(forms.Form):
	name = forms.CharField(max_length = 50)
	email = forms.EmailField(max_length = 100)
	password = forms.CharField(max_length = 50)
	repeat_password = forms.CharField(max_length = 50)
	
	def is_valid(self):
		valid = super(PersonForm, self).is_valid()
		if not valid:
			return valid
		if self.cleaned_data["password"] != self.cleaned_data["repeat_password"]:
			self._errors['Passwords do not match'] = 'Bad Password'
		person = Person.objects.filter(email = self.cleaned_data["email"])
		if person:
			self._errors["Email already in use"] = "Already email"
		return not self._errors
		
	#def __str__(self):
		
	
class LoginForm(forms.Form):
	email = forms.EmailField(max_length = 100)
	password = forms.CharField(max_length = 50)
	def is_valid(self):
		valid = super(LoginForm, self).is_valid()
		if not valid:
			return valid
		person = Person.objects.filter(email = self.cleaned_data["email"])
		if not person:
			self._errors["Email does not exist"] = "No email"
		if person and person[0].password != self.cleaned_data["password"]:
			self._errors["Incorrect Password"] = "Incorrect Password"
		return not self._errors