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
    text = forms.CharField(label=_("Start your text processing now!"),
                            widget=forms.TextInput ({
                                'class': 'form-control',
                                'placeholder':'Type or paste your text here...'}))


class TextEditorForm(forms.ModelForm):
    textinput=forms.CharField(label=_("Start your text processing now!"),
                            widget=forms.Textarea ({
                                'class': 'form-control',
                                'placeholder':'Type or paste your text here...'}))
    #save_as_docx=forms.BooleanField()#label=_("Check to save report as doc.x"))
    class Meta:
        model = TextEditor
        fields = ("textinput",)
