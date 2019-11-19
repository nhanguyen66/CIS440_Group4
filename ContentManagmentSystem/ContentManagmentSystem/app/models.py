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

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import language_check as lc

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

    #Creates a report of the difficulty reading level
    #Adds potential words to replace that are difficult 
    #List suggestions for each word
    #Lists troublesome sentences
    def check_difficulty(self):
        self.difficultyReport = "Error determining Difficulties"
    
    #summarizes the text using helper functions
    def summarize_text(self):
        self.summarizedText = generate_summary(self.textoutput)
        #try:
        #    self.summarizedText = generate_summary(self.textoutput)
        #except:
        #    self.summarizedText = "Error summarizing text"

    #generating the summary
    #takes in the corrected spelling text
    #returns a summary
    def generate_summary(text, top_n=5):
        stop_words = stopwords.words('english')
        summarize_text = []

        # Step 1 - Read text anc split it
        sentences = read_article(text)

        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        print("Indexes of top ranked_sentence order are ", ranked_sentence)

        for i in range(top_n):
            summarize_text.append(" ".join(ranked_sentence[i][1]))

        # Step 5 - Offcourse, output the summarize texr
        return summarize_text

    #gets the sentences
    def read_article(text):
        filedata = text
        article = filedata[0].split(". ")
        sentences = []

        for sentence in article:
            #print(sentence)
            sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        sentences.pop()
        return sentences

    def sentence_similarity(sent1, sent2, stopwords=None):
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


    def build_similarity_matrix(sentences, stop_words):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:  # ignore if both are same sentences
                    continue
                similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix


          
