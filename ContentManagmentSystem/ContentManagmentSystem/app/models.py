"""
Definition of models.
"""

from django.db import models

# Create your models here.

class TextEditor(models.Model):
    textinput = models.TextField(max_length=500)
    textoutput = "sample output"
    def __str__(self):
        return textinput
    def process_text(textinput):
        textoutput = textinput + "sdklaf"
