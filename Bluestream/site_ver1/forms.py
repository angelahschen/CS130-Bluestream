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
	options = (
		("Yes", "Yes"),
		("No", "No"),
	)
	options_NA = (
		("Yes", "Yes"),
		("No", "No"),
		("N/A", "N/A"),
	)
	options_Y_NA = (
		("Yes", "Yes"),
		("N/A", "N/A"),
	)
	options_onlyNA = (
		("N/A","N/A"),
	)
	RTA1_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA1_2 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA1_3 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA1_4 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA1_5 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA1_6 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	
	RTA2_1 = forms.MultipleChoiceField(choices=options,widget=forms.Select())
	RTA2_pg_1 = forms.CharField(label = "*page #", max_length = 50)
	RTA2_2 = forms.MultipleChoiceField(choices=options,widget=forms.Select())
	RTA2_pg_2 = forms.CharField(label = "*page #", max_length = 50)
	RTA2_3 = forms.MultipleChoiceField(choices=options,widget=forms.Select())
	RTA2_pg_3 = forms.CharField(label = "*page #", max_length = 50)
	RTA2_4 = forms.MultipleChoiceField(choices=options,widget=forms.Select())
	RTA2_pg_4 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_1 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_2_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_2_1 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_2_2 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_2_2 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_3 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_3 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_4 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_4 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_5 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_5 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_6 = forms.MultipleChoiceField(choices=options_Y_NA, widget=forms.Select())
	RTA3_pg_6 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_6_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_6_1 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_7 = forms.MultipleChoiceField(choices=options_Y_NA, widget=forms.Select())
	RTA3_pg_7 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_7_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_7_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_7_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_7_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_8 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_8 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_8_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_8_1 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_9 = forms.MultipleChoiceField(choices=options_Y_NA, widget=forms.Select())
	RTA3_pg_9 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_9_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_9_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_9_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_9_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_10 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_10 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_11_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_11_1 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_11_2 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_11_2 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_11_3 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_11_3 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_11_4 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_11_4 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_12 = forms.MultipleChoiceField(choices=options_Y_NA, widget=forms.Select())
	RTA3_pg_12 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_12_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_12_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_12_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_12_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_12_3 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_12_3 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_13_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_13_1 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_13_2 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_13_2 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_14_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_14_1 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_14_2 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_14_2 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_15 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_15 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_15_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_15_1 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_15_2 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_15_2 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_16 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_16 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_17 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_17 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_18 = forms.MultipleChoiceField(choices=options_Y_NA, widget=forms.Select())
	RTA3_pg_18 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_18_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_18_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_18_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_18_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_19 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_19 = forms.CharField(label = "*page #", max_length = 50)
	
	options_E = (
		("N/A", "N/A"),
		("Provided sterile, intended to be single-use", "Provided sterile, intended to be single-use"),
		("Requires processing during its use-life", "Requires processing during its use-life"),
		("Non-sterile when used and no processing required" ,"Non-sterile when used and no processing required"),
		("Information regarding the sterility status of the device is not provided (if this box is checked, please also check one of the two boxes below)", "Information regarding the sterility status of the device is not provided (if this box is checked, please also check one of the two boxes below)"),
		("Sterility status not needed for this device (e.g., software-only device)", " Sterility status not needed for this device (e.g., software-only device)"),
		("Sterility status needed or need unclear",  "Sterility status needed or need unclear"),
		("No", "No"),
	)
	RTA3_E = forms.MultipleChoiceField(choices = options_E,widget=forms.CheckboxSelectMultiple)
	RTA3_pg_E = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_20_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_20_1 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_20_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_20_2 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_20_3 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_20_3 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_21 = forms.MultipleChoiceField(choices=options_onlyNA, widget=forms.CheckboxSelectMultiple(), required=False)
	RTA3_pg_21 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_21_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_21_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_21_2 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_21_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_21_3 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_21_3 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_21_4 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_21_4 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_21_5 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_21_5 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_21_6 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_21_6 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_22 =forms.MultipleChoiceField(choices=options_onlyNA, widget=forms.CheckboxSelectMultiple(), required=False)
	RTA3_pg_22 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_22_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_22_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_22_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_22_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_22_3 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_22_3 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_22_4 = forms.MultipleChoiceField(choices=options_Y_NA, widget=forms.Select(), required=False)
	RTA3_pg_22_4 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_22_4_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_22_4_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_23 = forms.MultipleChoiceField(choices=options_Y_NA, widget=forms.Select())
	RTA3_pg_23 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_23_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_23_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_23_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_23_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_24 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_24 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_25 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_25 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_26 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_26 = forms.CharField(label = "*page #", max_length = 50)
	
	options_G = (
		("N/A", "N/A"),
		("Are direct or indirect patient-contacting components","Are direct or indirect patient-contacting components"),
		("Are no direct or indirect patient-contacting components","Are no direct or indirect patient-contacting components"),
		("Information regarding patient contact status of the device is not provided (if this box checked, please also check one of the two boxes below)","Information regarding patient contact status of the device is not provided (if this box checked, please also check one of the two boxes below)"),
		("Patient contact information not needed for this device (e.g., softwareonly device)","Patient contact information not needed for this device (e.g., softwareonly device)"),
		("Patient contact information is needed or need unclear","Patient contact information is needed or need unclear"),
		("No", "No"),
	)
	RTA3_G = forms.MultipleChoiceField(choices = options_E,widget=forms.CheckboxSelectMultiple)
	RTA3_pg_G = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_27 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_27 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_28 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_28 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_29 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_29 = forms.CharField(label = "*page #", max_length = 50)
	
	options_H = (
		("Does contain software/firmware","Does contain software/firmware"),
		("Does not contain software/firmware","Does not contain software/firmware"),
		("Information on whether device contains software/firmware is not provided (if this box checked, please also check one of the two boxes below)","Information on whether device contains software/firmware is not provided (if this box checked, please also check one of the two boxes below)"),
		("Software/firmware information not needed for this device (e.g., surgical suture, condom)","Software/firmware information not needed for this device (e.g., surgical suture, condom)"),
		("Software/firmware information is needed or need unclear","Software/firmware information is needed or need unclear"),
		("No", "No"),
	)
	RTA3_H = forms.MultipleChoiceField(choices = options_E,widget=forms.CheckboxSelectMultiple)
	RTA3_pg_H = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_30 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_30 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_31 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_31 = forms.CharField(label = "*page #", max_length = 50)
	
	options_I = (
		("Does require electrical safety evaluation","Does require electrical safety evaluation"),
		("Does not require electrical safety evaluation","Does not require electrical safety evaluation"),
		("Information on whether device requires electrical safety evaluation not provided (if this box checked, please also check one of the two boxes below)","Information on whether device requires electrical safety evaluation not provided (if this box checked, please also check one of the two boxes below)"),
		("Electrical safety information not needed for this device (e.g., surgical suture, condom)","Electrical safety information not needed for this device (e.g., surgical suture, condom)"),
		("Electrical safety information needed or need unclear","Electrical safety information needed or need unclear"),
		("No", "No"),
	)
	RTA3_I = forms.MultipleChoiceField(choices = options_I,widget=forms.CheckboxSelectMultiple())
	RTA3_pg_I = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_32 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_32 = forms.CharField(label = "*page #", max_length = 50)
	
	options_EMC = (
		("Does require EMC evaluation","Does require EMC evaluation"),
		("Does not require EMC evaluation","Does not require EMC evaluation"),
		("Information on whether device requires electrical safety evaluation not provided (if this box checked, please also check one of the two boxes below)","Information on whether device requires EMC not provided (if this box checked, please also check one of the two boxes below)"),
		("EMC information not needed for this device (e.g., surgical suture, condom)","EMC information not needed for this device (e.g., surgical suture, condom)"),
		("EMC information needed or need unclear","EMC information needed or need unclear"),
		("No", "No"),
	)
	RTA3_EMC = forms.MultipleChoiceField(choices = options_I,widget=forms.CheckboxSelectMultiple())
	RTA3_pg_EMC = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_33 = forms.MultipleChoiceField(choices=options, widget=forms.Select())
	RTA3_pg_33 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_J = forms.MultipleChoiceField(choices = options_onlyNA,widget=forms.CheckboxSelectMultiple())
	
	RTA3_34 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_34 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_34_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_34_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_35 = forms.MultipleChoiceField(choices=options_Y_NA, widget=forms.Select(), required=False)
	RTA3_pg_35 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_35_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_35_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_35_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_35_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_36 = forms.MultipleChoiceField(choices=options_onlyNA, widget=forms.CheckboxSelectMultiple(), required=False)
	RTA3_pg_36 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_36_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_36_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_36_2 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_36_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	RTA3_37 = forms.MultipleChoiceField(choices=options_onlyNA, widget=forms.CheckboxSelectMultiple(), required=False)
	RTA3_pg_37 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_37_1 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_37_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_37_2 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_37_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_37_3 = forms.MultipleChoiceField(choices=options, widget=forms.Select(), required=False)
	RTA3_pg_37_3 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	options_K = (
		("Is an in vitro diagnostic device","Is an in vitro diagnostic device"),
		("Is not an in vitro diagnostic device","Is not an in vitro diagnostic device"),
	)
	RTA3_K = forms.MultipleChoiceField(choices = options_K,widget=forms.CheckboxSelectMultiple())
	RTA3_pg_K = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_38_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_38_1 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_38_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_38_2 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_38_3 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_38_3 = forms.CharField(label = "*page #", max_length = 50)
	RTA3_38_4 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_38_4 = forms.CharField(label = "*page #", max_length = 50)
	
	RTA3_39 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select())
	RTA3_pg_39 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_39_1 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_39_1 = forms.CharField(label = "*page #", max_length = 50, required=False)
	RTA3_39_2 = forms.MultipleChoiceField(choices=options_NA, widget=forms.Select(), required=False)
	RTA3_pg_39_2 = forms.CharField(label = "*page #", max_length = 50, required=False)
	
	cvl = forms.CharField(widget=forms.Textarea, label='coverletter')

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