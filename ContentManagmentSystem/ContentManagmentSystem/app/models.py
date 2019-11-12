"""
Definition of models.
"""

from django.db import models
import cgi, cgitb
#from spellchecker import SpellChecker

# Create your models here.

class TextEditor(models.Model):
    textinput = models.TextField(max_length=500)
    textoutput = "sample output"
    def __str__(self):
        return textinput
    def process_text(textinput):
        textoutput = textinput + "sdklaf"

          


#form = cgi.FieldStorage()

#message = form.getvalue('message')

#message = "schol asignment due evry snday"

#split_message = message.split()

#spell = SpellChecker()

#new_message = spell.unknown(split_message)

#for word in new_message:
#  print(spell.correction(word))