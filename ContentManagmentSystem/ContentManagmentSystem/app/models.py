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
#import requests
import re
import string
from autocorrect import Speller
import spellcheck


# Create your models here.

class TextEditor(models.Model):
    textinput = models.TextField(blank=True)
    textoutput = "sample output"
    difficultyReport = ""
    summarizedText = ""

    testinput = """
    Why should I complete the Financial Readiness Score tool? (Expanded)
The FRS tool will give you knowledge and insight about your personal financial well-being. Think of this tool as your financial wellness navigator. We have various tools, products and services but the Financial Readiness Score tool is the only one that can give you a personalized action plan with specific tool recommendations to help improve your financial health.

Do I need to be a USAA member to get my Financial Readiness Score? (Expanded)
Yes, this is one of the many benefits in becoming a USAA member.

Why does USAA need my financial information when completing the Financial Readiness Score tool? (Expanded)
The purpose of the Financial Readiness Score tool is to provide an action plan to help each member become aware of his or her current financial well-being and how to help improve it. Without this information, the tool is not effective.

What if I don't agree with my score? (Expanded)
Your Financial Readiness Score is calculated based on a complex algorithm that takes in consideration over 13 different categories. One of the biggest reasons for a lower score tends to be from missing information, especially information on accounts you may have outside of USAA. The more information we have, the better we can serve you.

Will my Financial Readiness Score impact my FICO Credit Score? (Expanded)
No, your Financial Readiness Score is in no way connected to your FICO Credit Score.

How often should I check my Financial Readiness Score? (Expanded)
You only need to take the full assessment once. Your score and action plan will automatically update as you make progress on your actions. Depending on the specific action plan you may be on, it is a good habit to check back at least on a monthly basis to ensure you are on track and no new plans have arisen.

How do I access the Financial Readiness Score tool? (Expanded)
You need to be logged on to access the tool.
If you are already logged on: Select your name in the upper right corner and then select "My Financial Score."
If you haven’t logged in: Enter usaa.com/myfinancialscore in your browser and you will be able to log on.
Is the Financial Readiness Score tool available on the USAA Mobile App? (Expanded)
Yes:
If you have completed FRS: It will show up on your home page.
If you have not completed it: You can access it by selecting ‘More’ on the home page and you will see "Financial Score" as an option.
How long will it take to complete the assessment and get my score? (Expanded)
It typically takes 10 to 15 minutes to complete.

Why did USAA create this tool? (Expanded)
USAA’s core mission is to “facilitate the financial security of our members.” We believe we are placing that mission at the heart of this tool in order to empower our members to help understand and improve their finances and financial well-being.
"""

    def __str__(self):
        return textinput

    #testing
    def process_text(self):
        self.textoutput = self.testinput


    #replaces mispelled words
    def check_spelling(self):
        split_message = self.textoutput.translate(string.punctuation)
        split_message = self.textoutput.split(" ")
        spellc = SpellChecker()
        ss = Speller()

        misspelled = spellc.unknown(split_message);
        
        for word in misspelled:
            self.textoutput = self.textoutput#.replace(word, spellc.correction(word))


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


          
