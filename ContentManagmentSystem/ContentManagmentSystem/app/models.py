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
import nltk
nltk.download('stopwords')
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
        output = """
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
        self.summarizedText = self.generate_summary(self, output)
        #try:
        #    self.summarizedText = generate_summary(self.textoutput)
        #except:
        #    self.summarizedText = "Error summarizing text"








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


          
