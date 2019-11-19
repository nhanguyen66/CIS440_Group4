"""
Definition of forms.

SAMPLE TEXTS:

short samples:
Discover how well we can take care of you today. Members who switched saved an average of $707 a year

paragraph:
The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.

with new lines:
Protection for You and Your Passengers
Depending on where you live, how much you drive and what your health insurance covers, the amount of protection you need for each of these can vary:

Personal Injury Protection 
Extended Benefits Coverage
Uninsured and Underinsured Motorist Bodily Injury Coverage
Uninsured and Underinsured Motorist Property Damage Coverage
Note: The amount you choose for these types of car insurance coverage must be the same for each vehicle on your policy.

Roadside Assistance
Pays toward the cost to tow or repair your vehicle if you are stranded and your vehicle won't run. It also includes services to unlock your vehicle, deliver gas or change a tire.

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


class TextEditorForm(forms.ModelForm):
    textinput=forms.CharField(label=_("Text Input"),
                            widget=forms.Textarea ({
                                'class': 'form-control',
                                'placeholder':'Type or paste your text'}))
    class Meta:
        model = TextEditor
        fields = ("textinput",)
