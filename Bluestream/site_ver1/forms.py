import datetime
from django import forms

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
# BoundField is imported for backwards compatibility in Django 1.9
from django.forms.boundfield import BoundField  # NOQA
from django.forms.fields import Field, FileField
# pretty_name is imported for backwards compatibility in Django 1.9
from django.forms.utils import ErrorDict, ErrorList, pretty_name  # NOQA
from django.forms.widgets import Media, MediaDefiningClass
from django.utils.functional import cached_property
from django.utils.html import conditional_escape, html_safe
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from .models import Person
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
MAX_PASS_LENGTH = 20
MAX_NAME_LENGTH = 50
MAX_PROJ_LENGTH = 100

class myForm(forms.Form):
	def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        #"Output HTML. Used by as_table(), as_ul(), as_p()."
		top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
		output, hidden_fields = [], []
		for name, field in self.fields.items():
			html_class_attr = ''
			bf = self[name]
			# Escape and cache in local variable.
			bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
			if bf.is_hidden:
				if bf_errors:
					top_errors.extend(
						[_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': str(e)}
						for e in bf_errors])
				hidden_fields.append(str(bf))
			else:
				# Create a 'class="..."' attribute if the row should have any
				# CSS classes applied.
				css_classes = bf.css_classes()
				if css_classes:
					html_class_attr = ' class="%s"' % css_classes

				if errors_on_separate_row and bf_errors:
					output.append(error_row % str(bf_errors))

				if bf.label:
					label = conditional_escape(bf.label)
					label = bf.label_tag(label) or ''
				else:
					label = ''

				if field.help_text:
					help_text = help_text_html % field.help_text
				else:
					help_text = ''
				if hasattr(self, 'cleaned_data'):
					if name in self.cleaned_data:
						value = self.cleaned_data[name]
					else:
						value = ''
				else:
					value = ''
				output.append(normal_row % {
					'errors': bf_errors,
					'label': label,
					'field': bf,
					'help_text': help_text,
					'html_class_attr': html_class_attr,
					'css_classes': css_classes,
					'field_name': bf.html_name,
					'name': name,
					'value': value,
				})

		if top_errors:
			output.insert(0, error_row % top_errors)

		if hidden_fields:  # Insert any hidden fields in the last row.
			str_hidden = ''.join(hidden_fields)
			if output:
				last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
				if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
					last_row = (normal_row % {
						'errors': '',
						'label': '',
						'field': '',
						'help_text': '',
						'html_class_attr': html_class_attr,
						'css_classes': '',
						'field_name': '',
					})
					output.append(last_row)
				output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
			else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
				output.append(str_hidden)
		return mark_safe('\n'.join(output))
class PersonForm(myForm):
	name = forms.CharField(max_length = 50)
	email = forms.EmailField(max_length = 100)
	password = forms.CharField(max_length = 50)
	repeat_password = forms.CharField(max_length = 50)
	options = (
		("C", "Client"),
		("R", "Regulatory Consultant"),
	)
	role = forms.MultipleChoiceField(choices = options)
	phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', help_text="Format: +##########")
	def is_valid(self):
		valid = super(PersonForm, self).is_valid()
		if not valid:
			return valid
		if self.cleaned_data["password"] != self.cleaned_data["repeat_password"]:
			self._errors['Passwords do not match'] = 'Bad Password'
		person = User.objects.filter(username = self.cleaned_data["email"])
		if person:
			self._errors["Email already in use"] = "Already email"
		return not self._errors
class LoginForm(myForm):
	email = forms.EmailField(max_length = 100)
	password = forms.CharField(max_length = 50)
	def is_valid(self):
		valid = super(LoginForm, self).is_valid()
		if not valid:
			return valid
		user = authenticate(username=self.cleaned_data["email"], password = self.cleaned_data["password"])
		if not user:
			self._errors["Incorrect Account Data"] = "Wrong Login"
		return not self._errors
	
	def __str__(self):
		return self._html_output(normal_row = '<div class="form-group"><input class="form-control" placeholder=%(name)s name=%(name)s autofocus></div>',
			error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='',
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)
			
class ProjectForm(myForm):
	proj_name = forms.CharField(max_length = MAX_PROJ_LENGTH)
	business_name = forms.CharField(max_length = MAX_PROJ_LENGTH)
	email_recipient = forms.EmailField(max_length=MAX_PROJ_LENGTH, required = False)	
	def __str__(self):
		return self._html_output(normal_row = '<div class="form-group"><input class="form-control" placeholder=%(name)s name=%(name)s autofocus></div>',
			error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='',
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)
			
	def is_valid(self):
		valid = super(ProjectForm, self).is_valid()
		if not valid:
			return valid
		if self.cleaned_data["email_recipient"] != '':
			users = User.objects.filter(username = self.cleaned_data["email_recipient"])
			if not users:
				self._errors["No account exists with that email"] = True
				return False
			is_client = False
			for user in users:
				if user.person.role == "C":
					is_client = True
				break
			if not is_client:
				self._errors["You cannot assign projects to Regulatory Consultants"] = True
		return not self._errors


class CoverLetterForm(forms.Form):
	cvl = forms.CharField(widget=forms.Textarea, label='coverletter', required=False)

class Section4Form(forms.Form):
	number = forms.CharField(label = '510K Number (if known)', max_length = 50, required=False)
	device_name = forms.CharField(max_length = 50)
	indication = forms.CharField(widget=forms.Textarea, label = 'Indications for use (Describe)')

class Section5Form(forms.Form):
	options = (
		("510ksummary", "510K-Summary"),
		("510kstatement", "510K-Statement"),
	)
	my_field = forms.ChoiceField(choices=options, label="",widget=forms.CheckboxSelectMultiple())
	summary = forms.CharField(widget=forms.Textarea, label = 'summary')


class Section6Form(forms.Form):
	position = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Position held in company'}))
	company_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
	signiture = forms.CharField()
	submitter_name =forms.CharField()
	date= forms.DateField(initial=datetime.date.today)
	number = forms.CharField(max_length = 50, required=False)

class Section7Form(forms.Form):
	position = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Position in company'}))
	company_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
	device_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Device Name'}))
	summary_data = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Attach the summary of problem data, bibliography or other citations upon which the summary is based.', 'rows':20, 'cols':80}))
	signiture = forms.CharField()
	certifier_name =forms.CharField()
	date= forms.DateField(initial=datetime.date.today)
	number = forms.CharField(max_length = 50, required=False)


class Section8Form(forms.Form):
	certification = forms.FileField(label = "Select a file")
	disclosure = forms.FileField(label = "Select a file")
