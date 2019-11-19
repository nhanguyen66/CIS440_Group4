"""
Definition of models.
"""

"""
Aoccdrnig to a rscheearch at Cmabrigde Uinervtisy, it deosn’t mttaer in waht oredr the ltteers in a wrod are, the olny iprmoetnt tihng is taht the frist and lsat ltteer be at the rghit pclae. The rset can be a total mses and you can sitll raed it wouthit a porbelm. Tihs is bcuseae the huamn mnid deos not raed ervey lteter by istlef, but the wrod as a wlohe. Amzanig huh?
"""
from django.db import models
import cgi, cgitb
from spellchecker import SpellChecker
import cgi, cgitb

# Create your models here.

class TextEditor(models.Model):
    textinput = models.TextField(blank=True)
    textoutput = "sample output"
    difficultyReport = ""
    summarizedText = ""

    def __str__(self):
        return textinput

    #testing
    def process_text(self):
        self.textoutput = self.textinput + "!"
        self.textoutput = self.textoutput.replace("Discver","Discover",1)

    #replaces mispelled words
    def check_spelling(self):
        split_message = self.textinput.split()
        spell = SpellChecker()

        self.corrected_string = []
        stringsToCorrect = []
        for word in split_message:
            if spell._check_if_should_check(word):
                stringsToCorrect.append(word)

        for word in stringsToCorrect:
            self.textoutput = self.textoutput.replace(word,spell.correction(word),1)

            #self.corrected_string.append(spell.correction(word))
       
            #self.textoutput = ' '.join(self.corrected_string)

    #Creates a report of the difficulty reading level
    #Adds potential words to replace that are difficult 
    #List suggestions for each word
    #Lists troublesome sentences
    def check_difficulty(self):
        self.difficultyReport = "Error determining Difficulties"
    
    def summarize_text(self):
        self.summarizedText = "Error summarizing text"

"""
1) Create a list with mispelled words
2) For each mispelled word, 
string.self.textoutput = self.textoutput.replace(list[i],spell.correction(list[i]),1)
(basically replace every mispelled word with the correct spelling)

"""
      
          
