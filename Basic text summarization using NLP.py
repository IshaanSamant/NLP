import nltk
import math
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
from string import punctuation
import string
stop_words = set(stopwords.words('English'))
wordlemmatizer = WordNetLemmatizer()
#reading the paragraph from a text file and assigning it to a variable
f = open('pro.txt', 'r')
document = f.read()
f.close()
#list meant for modification
sentences_list = sent_tokenize(document)
#this list is an unaltered list meant for the output
sentences_list1 = sent_tokenize(document)

#travesring through the paragraph characterwise and removing all the puncutations
for i in range(len(sentences_list)):
   sentences_list[i]=''.join(c for c in sentences_list[i] if c not in punctuation)
#a function that returns words that are eitheir nouns or verbs, which are the words with the highest relelvance
def pos_tagging(text):
    pos_tag = nltk.pos_tag(text.split())
    pos_tagged_noun_verb = []
    for word,tag in pos_tag:
        if tag == "NN" or tag == "NNP" or tag == "NNS" or tag == "VB" or tag == "VBD" or tag == "VBG" or tag == "VBN" or tag == "VBP" or tag == "VBZ":
             pos_tagged_noun_verb.append(word)
    return pos_tagged_noun_verb
#function to calculate the idf score of a given word, in this case idf is not inter document but is calculated between different sentences
#it is calcualted as the logarithm of the division of the total number of sentences divided by the number of sentences in which the given word occurs
def idf_score(word,sentences):
    no_of_sentence_containing_word = 0
    for sentence in sentences:
        #converting the temporary variable into a list of words to make it easier to pick only the desired words
        sentence = sentence.split()
        #removing stop words and words with only one letter because they are useless words which don't contribute to the information in a sentence
        sentence = [word for word in sentence if word.lower() not in stop_words and len(word)>1]
        #converting each word in sentence to lower to avoid same words with different capitalization to be treated as the same word
        sentence = [word.lower() for word in sentence]
        #lemmenaitzer is to find the root of the given words to avoid confusion between different derivatives of the same word
        sentence = [wordlemmatizer.lemmatize(word) for word in sentence]
        if word in sentence:
            #counting the frequency sentences in which the word is present
            no_of_sentence_containing_word = no_of_sentence_containing_word + 1
    idf = math.log10(len(sentences)/no_of_sentence_containing_word)
    return idf
#function to calculate the term frequency of a word in a sentence
def tf_score(word,sentence):
    freq_sum = 0
    word_frequency_in_sentence = 0
    len_sentence = len(sentence)
    for word_in_sentence in sentence.split():
        if word == word_in_sentence:
            word_frequency_in_sentence = word_frequency_in_sentence + 1
    tf =  word_frequency_in_sentence/ len_sentence
    return tf
#function to calculate the score of a given line
def sentence_importance(sentence,sentences):
     sentence_score = 0
     pos_tagged_sentence = [] 
     no_of_sentences = len(sentences)
     #assigning the post tagged sentence to a variable
     pos_tagged_sentence = pos_tagging(sentence)
     for word in pos_tagged_sentence:
          if word.lower() not in stop_words and len(word)>1: 
                word = word.lower()
                #lemmenaitzer is to find the root of the given words to avoid confusion between different derivatives of the same word
                word = wordlemmatizer.lemmatize(word)
                #sentence score is the summation of the tdif of the relavent words in the sentence(tdif value if the product of the tf and idf values of a given word)
                sentence_score = sentence_score + tf_score(word,sentence)*idf_score(word,sentences)
     return sentence_score
#and array to store the score of every sentence
score=[]
#running the score program for every sentence in the pragraph
for i in sentences_list:
    score.append(sentence_importance(i,sentences_list))
m=0
#m stores the index of the line with the highes score
for i in range(len(sentences_list)):
    if score[m]<score[i]:
        m=i
#prints the original version of the line with the greatest score
print(sentences_list1[m])
