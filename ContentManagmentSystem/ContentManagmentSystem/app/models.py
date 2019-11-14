"""
Definition of models.
"""

from django.db import models
import cgi, cgitb
from spellchecker import SpellChecker
import cgi, cgitb

# Create your models here.

class TextEditor(models.Model):
    textinput = models.TextField(max_length=500)
    textoutput = "sample output"

    def __str__(self):
        return textinput

    def process_text(self):
        self.textoutput = self.textinput + "!"

    def check_spelling(self):
        split_message = self.textoutput.split()
        spell = SpellChecker()
        
        self.corrected_string = []
        for word in split_message:
            self.corrected_string.append(spell.correction(word))
       
        self.textoutput = ' '.join(self.corrected_string)
        
      
          
