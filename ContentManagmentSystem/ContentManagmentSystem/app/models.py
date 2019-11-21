"""
Definition of models.
"""

from django.db import models
import cgi, cgitb
from spellchecker import SpellChecker
import cgi, cgitb
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import language_check as lc
import textstat
import requests
import re

# Create your models here.

class TextEditor(models.Model):
    textinput = models.TextField(blank=True)
    textoutput = "sample output"
    difficultyReport = ""
    summarizedText = ""

    testinput = """
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

    def __str__(self):
        return textinput

    #testing
    def process_text(self):
        #self.textoutput = self.textinput + "!"
        self.textoutput = self.testinput + "!"


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
        self.textoutput = self.textoutput.replace("Discver","Discover",1)


    #Creates a report of the difficulty reading level
    #Adds potential words to replace that are difficult 
    #List suggestions for each word
    #Lists troublesome sentences
    def check_difficulty(self):
        text = self.textoutput
            #0-30 = college
            #50-60 = high school
            #60+ = middle school/elementary school
        try:
            grade_level = textstat.text_standard(text)
            reading_ease = textstat.flesch_reading_ease(text) #requires chart
            sentence_count = textstat.sentence_count(text)
            difficult_words = self.get_difficult_words(text)
            replacement_words = self.get_replacement_words(difficult_words)
            output = "Grade Level of Input Text: " + grade_level + "\n"
            #output = output + "Ease of Reading*: " + str(reading_ease) + "\n"
            output = output + "Sentence Count: " + str(sentence_count) + "\n"
            output = output + "Difficult Words Found: " + str(len(difficult_words)) + "\n"
            output = output + "Possible Replacements: " + "\n"
            for dw in replacement_words:
                output = output + dw + " -> "
                for word in replacement_words[dw]:
                    output = output + word + ", "
                output = output + "\n"
            self.difficultyReport = output
        except:
            self.difficultyReport = "Error determining Difficulties"
    

    def get_difficult_words(self, input):
        #https://stackoverflow.com/questions/54710198/getting-out-difficult-english-words-from-text-for-vocabulary-building-using-pyth
        english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
        # Get the file of 10 k most common words from TXT file in a github repo
        response = requests.get(english_most_common_10k)
        data = response.text
        set_of_common_words = {x for x in data.split('\n')}
        common_words = []
        difficult_words = []

        #accounting for verbs that end in s...
        for word in set_of_common_words:
            common_words.append(word)
            common_words.append(word + "s")

        text = input.strip().replace("\n", " ").replace("."," ").split(" ")
        
        for word in text:
            w = word.strip().lower()
            w = re.sub('[^a-zA-Z\']','',w)
            if w not in common_words:       
                difficult_words.append(word)
        return difficult_words

    def get_replacement_words(self, difficult_words):
        english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
        # Get the file of 10 k most common words from TXT file in a github repo
        response = requests.get(english_most_common_10k)
        data = response.text
        set_of_common_words = {x for x in data.split('\n')}
        
        dictionary = {}

        for word in difficult_words:
            w = word.strip().lower()
            w = re.sub('[^a-zA-Z\']','',w)
            s = []
            #go through all synonyms
            for syn in wordnet.synsets(w):
                sl = syn.lemmas()
                for l in sl:
                    ll = l.name()
                    if ll not in s:
                    #checking against smaller list first
                    #if ll in set_of_common_words and ll not in s:
                        s.append(ll)
            #add list of synonyms to dictionary
            dictionary[word] = s

        return dictionary


    #summarizes the text using helper functions
    #idk how this function works
    #takes the input text and gets top n phrases
    #returns a list of the top n phrases
    def summarize_text(self):
        text = self.testinput   
        try:
            self.summarizedText = self.generate_summary(self, text)
        except:
            self.summarizedText = "Error summarizing text"


    #generating the summary
    #takes in the corrected spelling text
    #returns a summary
    def generate_summary(self, thing, input, top_n=5):
        stop_words = stopwords.words('english')
        summarize_text_list = []

        # Step 1 - Read text anc split it
        sentences = self.read_article(input)

        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = self.build_similarity_matrix(sentences, stop_words)

        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph,max_iter = 100000)

        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        #print("Indexes of top ranked_sentence order are ", ranked_sentence)

        for i in range(top_n):
            sentence = " ".join(ranked_sentence[i][1])
            summarize_text_list.append(sentence + ".")

        res = []
        [res.append(x) for x in summarize_text_list if x not in res]
        #summarize_text_list = res

        # Step 5 - Offcourse, output the summarize texr
        return summarize_text_list



    #"read article"
    #returns a list of sentences
    def read_article(self, input):
        filedata = input
        filedata = filedata.replace('\n','.')
        article = filedata.split(".")
        sentences = []

        for sentence in article:
            if(sentence != '' and sentence !='.'):
                s = sentence.strip()
                s = s.replace("[^a-zA-Z]", " ")
                s = s.split(" ")
                sentences.append(s)
        #sentences.pop()
        return sentences


    #get sentence similarity
    def sentence_similarity(self, sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = []

        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]

        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        # build the vector for the first sentence
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1

        # build the vector for the second sentence
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1

        return 1 - cosine_distance(vector1, vector2)



    #built dimilarity matrix
    def build_similarity_matrix(self, sentences, stop_words):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:  # ignore if both are same sentences
                    continue
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix


          
