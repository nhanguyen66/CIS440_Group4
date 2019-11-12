"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import TextEditor

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    text = forms.CharField(label=_("Text Input"),
                            widget=forms.TextInput ({
                                'class': 'form-control',
                                'placeholder':'Type or paste your text'}))

#class ProcessText(forms.Form):
#    """Authentication form which uses boostrap CSS."""
#    text_input = forms.Textarea(max_lenth=900, required = True, help_text = "enter text")

class TextEditorForm(forms.ModelForm):
    textinput=forms.CharField(label=_("Text Input"),
                            widget=forms.TextInput ({
                                'class': 'form-control',
                                'placeholder':'Type or paste your text'}))
    class Meta:
        model = TextEditor
        fields = ("textinput",)
