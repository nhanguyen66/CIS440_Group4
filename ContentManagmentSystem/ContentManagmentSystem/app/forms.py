"""
Definition of forms.

SAMPLE TEXTS:

short samples:
Discver how well we can take cre of you tday. Members who switched saved an average of $707 a year

paragraph:
The qick brown fx jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.

with new lines:
Protection for u and Your Pasengers
Depending on where you live, how much you drive and what your health insurance covers, the amount of protection you need for each of these can vary:

Personal Injury Protection 
Exended Beneits Covege
Unnsured and Underinsured Motorist Bodily Injury Coverage
Unnsured and Underinsured Motorist Property Damage Coverage
Nte: The amount you choose for these types of car insurance coverage must be the same for each vehicle on your policy.

Radside Assistance
Pys toward the cost to tow or repair your vehicle if you are stranded and your vehicle won't run. It also includes services to unlock your vehicle, deliver gas or change a tire.

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
    class Meta:
        model = TextEditor
        fields = ("textinput",)
