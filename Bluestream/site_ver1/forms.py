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
class PersonForm(forms.Form):
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
		person = Person.objects.filter(email = self.cleaned_data["email"])
		if person:
			self._errors["Email already in use"] = "Already email"
		return not self._errors
	
	'''def __str__(self):
		return self._html_output(normal_row = '<div class="form-group"><span class="help-block">%(help_text)s</span><input class="form-control"  placeholder=%(name)s name=%(name)s autofocus value=%(value)s></div>',
			error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='',
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)
	def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        #"Output HTML. Used by as_table(), as_ul(), as_p()."
		top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
		output, hidden_fields = [], []
		print(self.data)
		if hasattr(self, 'cleaned_data'):
			print(self.cleaned_data)
		for name, field in self.fields.items():
			html_class_attr = ''
			bf = self[name]
			#print(self.cleaned_data)
			#print(self.cleaned_data[name])
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
				print(name, value)
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
		return mark_safe('\n'.join(output))'''
	
		
	
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
	
	def __str__(self):
		#return "hi"
		#print(self.fields)
		return self._html_output(normal_row = '<div class="form-group"><input class="form-control" placeholder=%(name)s name=%(name)s autofocus></div>',
			error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='',
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)
			
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

				output.append(normal_row % {
					'errors': bf_errors,
					'label': label,
					'field': bf,
					'help_text': help_text,
					'html_class_attr': html_class_attr,
					'css_classes': css_classes,
					'field_name': bf.html_name,
					'name': name,
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
		