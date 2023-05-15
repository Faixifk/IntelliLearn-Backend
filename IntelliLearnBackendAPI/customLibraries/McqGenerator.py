import unicodedata
import nltk
nltk.download('stopwords')
nltk.download('popular')
import pprint
import itertools
import re
import pke
import string
from nltk.corpus import stopwords
from summarizer import Summarizer
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
import requests
import json
import re
import random
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet as wn

class MCQ_Generator:
    
    def __init__(self):
        
        pass
    
    def summarize_paragraph(self, paragraph):
        
        '''
            Summarize a paragraph to pick up most important sentences only.
            
        '''
        model = Summarizer()
        result = model(paragraph, min_length=60, max_length = 500 , ratio = 0.3)

        summarized_text = ''.join(result)
        
        return summarized_text
    
    def get_nouns_multipartite(self, text, n = 20):
        out=[]

        extractor = pke.unsupervised.MultipartiteRank()
        #    not contain punctuation marks or stopwords as candidates.
        pos = {'PROPN'}
        #pos = {'VERB', 'ADJ', 'NOUN'}
        stoplist = list(string.punctuation)
        stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        stoplist += stopwords.words('english')
        extractor.load_document(input=text, stoplist=stoplist)
        extractor.candidate_selection(pos=pos, )
        # 4. build the Multipartite graph and rank candidates using random walk,
        #    alpha controls the weight adjustment mechanism, see TopicRank for
        #    threshold/method parameters.
        extractor.candidate_weighting(alpha=1.1,
                                      threshold=0.75,
                                      method='average')
        keyphrases = extractor.get_n_best(n=n)

        for key in keyphrases:
            out.append(key[0])

        return out
        
    def tokenize_sentences(self, text):
        sentences = [sent_tokenize(text)]
        sentences = [y for x in sentences for y in x]
        # Remove any short sentences less than 20 letters.
        sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
        return sentences

    def get_sentences_for_keyword(self, keywords, sentences):
        keyword_processor = KeywordProcessor()
        keyword_sentences = {}
        for word in keywords:
            keyword_sentences[word] = []
            keyword_processor.add_keyword(word)
        for sentence in sentences:
            keywords_found = keyword_processor.extract_keywords(sentence)
            for key in keywords_found:
                keyword_sentences[key].append(sentence)

        for key in keyword_sentences.keys():
            values = keyword_sentences[key]
            values = sorted(values, key=len, reverse=True)
            keyword_sentences[key] = values
        return keyword_sentences
    

    # Distractors from Wordnet
    def get_distractors_wordnet(self, syn,word):
        distractors=[]
        word= word.lower()
        orig_word = word
        if len(word.split())>0:
            word = word.replace(" ","_")
        hypernym = syn.hypernyms()
        if len(hypernym) == 0: 
            return distractors
        for item in hypernym[0].hyponyms():
            name = item.lemmas()[0].name()
            #print ("name ",name, " word",orig_word)
            if name == orig_word:
                continue
            name = name.replace("_"," ")
            name = " ".join(w.capitalize() for w in name.split())
            if name is not None and name not in distractors:
                distractors.append(name)
        return distractors

    def get_wordsense(self, sent,word):
        word= word.lower()

        if len(word.split())>0:
            word = word.replace(" ","_")


        synsets = wn.synsets(word,'n')
        if synsets:
            wup = max_similarity(sent, word, 'wup', pos='n')
            adapted_lesk_output =  adapted_lesk(sent, word, pos='n')
            lowest_index = min (synsets.index(wup),synsets.index(adapted_lesk_output))
            return synsets[lowest_index]
        else:
            return None

    # Distractors from http://conceptnet.io/
    def get_distractors_conceptnet(self, word):
        word = word.lower()
        original_word= word
        if (len(word.split())>0):
            word = word.replace(" ","_")
        distractor_list = [] 
        url = "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5"%(word,word)
        obj = requests.get(url).json()

        for edge in obj['edges']:
            link = edge['end']['term'] 

            url2 = "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"%(link,link)
            obj2 = requests.get(url2).json()
            for edge in obj2['edges']:
                word2 = edge['start']['label']
                if word2 not in distractor_list and original_word.lower() not in word2.lower():
                    distractor_list.append(word2)

        return distractor_list
    
    #some preprocessing functions
    def remove_substrings_with_dot_question(self, text):
        
        '''
            Input: string
            Output: String with all questions removes (Sentences ending at '?')

            Process: 
                a) Remove Questions from the book (lines between . and ?)

        '''

        pattern = r'\.[^.]*\?'

        # Remove substrings matching the pattern
        result = re.sub(pattern, '', text)

        return result

    def remove_words_no_lowercase(self, text):

        '''
            Input: string
            Output: String with only the words that contain at least one lowercase letter
                    Since the word with only uppercase letters are headings

            Process: 
                a) Remove words with 0 lowercase letters and at least 3 characters in total (to avoid removing units such as J for Joules)

        '''

        words = text.split()
        result = [word for word in words if sum(1 for c in word if c.isupper()) < 4]
        return ' '.join(result)

    def remove_unicode_characters(self, text):
        return ''.join(char for char in text if unicodedata.category(char)[0] != 'C')

    def remove_punctuation(self, text):
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def preprocess_text(self, extracted_text):
                
        processed_text = self.remove_substrings_with_dot_question(extracted_text)
        processed_text = self.remove_unicode_characters(processed_text)
        processed_text = self.remove_words_no_lowercase(processed_text)
        #processed_text = self.remove_punctuation(processed_text)
        
        return processed_text

    #main function of the class
    def generate_MCQS(self, txt_content):
        
        #f = open(txt_file,"r", encoding='utf-8')
        #full_text = f.read()
        
        full_text = txt_content

        print("Length before preprocessing: ", len(full_text))
        #preprocess
        full_text = self.preprocess_text(full_text)
        print("Length after preprocessing: ", len(full_text))
        print(full_text)
        summarized_text = self.summarize_paragraph(full_text)
        print (summarized_text)
        print("Length after summarizing: ", len(summarized_text))
        
        keywords = self.get_nouns_multipartite(full_text) 
        print (keywords)
        
        filtered_keys=[]
        for keyword in keywords:
            if keyword.lower() in summarized_text.lower():
                filtered_keys.append(keyword)

        print (filtered_keys)
       
        sentences = self.tokenize_sentences(summarized_text)
        keyword_sentence_mapping = self.get_sentences_for_keyword(filtered_keys, sentences)

        print (keyword_sentence_mapping)
        
        for keyword in keyword_sentence_mapping:
            print(keyword, " ", str(len(keyword_sentence_mapping[keyword])))
        
        key_distractor_list = {}

        for keyword in keyword_sentence_mapping:

            print("Keyword [", keyword, '] processed..')

            if len(keyword_sentence_mapping[keyword]) == 0:
                continue
            
            wordsense = self.get_wordsense(keyword_sentence_mapping[keyword][0],keyword)
            print("Got wordsense")
            if wordsense:
                distractors = self.get_distractors_wordnet(wordsense,keyword)
                print("Got distractors")
                
                if len(distractors) ==0:
                    distractors = self.get_distractors_conceptnet(keyword)
                if len(distractors) != 0:
                    key_distractor_list[keyword] = distractors
            else:
                print("Got no distractors")

                distractors = self.get_distractors_conceptnet(keyword)
                if len(distractors) != 0:
                    key_distractor_list[keyword] = distractors

        index = 1

        mcqs = []
        
        print("Creating mcqs with distractors..")
        for each in key_distractor_list:
            print("Getting distractors for ", each)
            sentence = keyword_sentence_mapping[each][0]
            pattern = re.compile(each, re.IGNORECASE)
            output = pattern.sub( " _______ ", sentence)
            print ("%s)"%(index),output)
            choices = [each.capitalize()] + key_distractor_list[each]
            top4choices = choices[:4]
            random.shuffle(top4choices)
            optionchoices = ['a','b','c','d']
            for idx,choice in enumerate(top4choices):
                print ("\t",optionchoices[idx],")"," ",choice)
            print ("\nMore options: ", choices[4:20],"\n\n")
            index = index + 1
            
            extra_options = ['All of these', 'None of these', 'Not sure', 'Skip']
            random.shuffle(extra_options)
            
            while len(top4choices) < 4:
                top4choices.append(extra_options[0])
                extra_options.pop(0)
            
            mcqs.append({"question": output, "option_a":top4choices[0], "option_b":top4choices[1], 
                         "option_c":top4choices[2], "option_d":top4choices[3], "correct_option": each})


        print("Returning mcqs list of length ", str(len(mcqs)))
        return mcqs