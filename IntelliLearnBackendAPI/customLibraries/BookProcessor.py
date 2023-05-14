import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
from transformers import BertForQuestionAnswering
import torch
import PyPDF2
from transformers import pipeline
import unicodedata
import string
from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer

class BookProcessor:
    
    #Improvement can be added by adding redundant chunks, i.e. 0 - 400, 200 - 600, 400 - 800, 600 - 1000, etc..
    #Another approach is to group relevant sentences in chunks together. Given a question, sort these chunks instead of original ones
    
    def __init__(self):
        self.model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        #self.model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased')
        #self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')


        nltk.download('punkt')
        self.tfidf_vectorizer = TfidfVectorizer()
    
    def convert_pdf_to_string(self, pdf_path, output_path):
        # Open the PDF file in read-binary mode

        with open('D:/IntelliLearn Backend/books/'+pdf_path, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Initialize an empty string to store the extracted text
            extracted_text = ''

            # Iterate over each page in the PDF
            for page_num in range(len(pdf_reader.pages)):
                # Get the current page
                page = pdf_reader.pages[page_num]

                # Extract the text from the page
                text = page.extract_text()

                # Append the extracted text to the overall text
                extracted_text += text

        return extracted_text
    

    # Step 1: Splitting the book into chunks
    def split_book_into_chunks(self, book_text, chunk_size):
        # Tokenize the book text into words
        words = nltk.word_tokenize(book_text)

        # Initialize variables
        current_chunk = []
        chunks = []

        for word in words:
            # If adding the current word would exceed the desired chunk size,
            # finalize the current chunk and start a new one
            if len(current_chunk) + 1 > chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))

                current_chunk = []
            # Add the word to the current chunk
            current_chunk.append(word)

        # Add the last chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    # Step 2: Indexing the chunks
    def create_chunk_index(self, chunks):
        # Create an index dictionary to store chunk metadata
        index = {}

        # Iterate over the chunks and create the index
        for i, chunk in enumerate(chunks):
            # Store the chunk metadata (in this case, the chunk itself)
            index[i] = chunk

        return index
    
    # Step 3: Preprocessing the question
    def preprocess_question(self, question):
        # Tokenize the question
        tokenizer = nltk.tokenize.WordPunctTokenizer()
        tokens = tokenizer.tokenize(question)

        # Perform any additional preprocessing steps (e.g., lowercasing, removing stopwords)

        preprocessed_question = ' '.join(tokens)
        return preprocessed_question
    
    # Step 4: Identifying relevant chunks
    def find_relevant_chunks(self, question, index):
        # Create a TF-IDF vectorizer and fit it on the chunks
        tfidf_vectorizer = self.tfidf_vectorizer
        chunk_texts = list(index.values())
        tfidf_matrix = tfidf_vectorizer.fit_transform(chunk_texts)

        # Transform the preprocessed question into a TF-IDF vector
        preprocessed_question_vector = tfidf_vectorizer.transform([question])

        # Calculate cosine similarities between the question vector and chunk vectors
        similarities = cosine_similarity(preprocessed_question_vector, tfidf_matrix)

        # Sort the chunks based on similarity scores
        sorted_chunks = [chunk for _, chunk in sorted(zip(similarities[0], chunk_texts), reverse=True)]

        # Return the relevant chunks
        return sorted_chunks

    # Step 5: Identifying topic boundaries
    def identify_topic_boundaries(self, chunks):
        # Implement the logic to identify topic boundaries using topic modeling or other techniques
        # This implementation uses a simple approach based on the number of sentences per topic

        # Set the threshold for the maximum number of sentences allowed in a topic
        max_sentences_per_topic = 5

        topic_boundaries = []

        # Iterate over the chunks and identify topic boundaries
        for chunk in chunks:
            # Tokenize the chunk into sentences
            sentences = nltk.sent_tokenize(chunk)

            # Check if the number of sentences exceeds the threshold
            if len(sentences) > max_sentences_per_topic:
                # Add the index of the last sentence as a topic boundary
                topic_boundaries.append(len(topic_boundaries))

        return topic_boundaries
    

    # Step 6: Answering the question
    def answer_question(self, question, relevant_chunks):
        # Implement the logic to use BERT for question answering on the relevant chunks
        # This implementation assumes you have a pretrained BERT model and tokenizer

        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

        answers = []

        for chunk in relevant_chunks:
            # Tokenize the chunk and question
            tokenized_chunk = tokenizer.encode(chunk, add_special_tokens=True, truncation=True, max_length=512)
            tokenized_question = tokenizer.encode(question, add_special_tokens=True, truncation=True, max_length=512)

            # Check if the combined tokens exceed the maximum length
            if len(tokenized_chunk) + len(tokenized_question) > 512:
                # Truncate the chunk to fit within the maximum length
                remaining_space = 512 - len(tokenized_question) - 3  # Account for [CLS], [SEP], [SEP] tokens
                tokenized_chunk = tokenized_chunk[:remaining_space]

            # Create the input tensors
            input_ids = torch.tensor([tokenized_chunk + tokenized_question[1:]], dtype=torch.long)
            attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

            # Pass the input tensors through the BERT model
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)

            # Retrieve the start and end logits from the model outputs
            start_logits = outputs.start_logits
            end_logits = outputs.end_logits

            # Find the start and end positions with the highest logits
            start_pos = torch.argmax(start_logits)
            end_pos = torch.argmax(end_logits)

            # Convert the predicted token indices to actual tokens
            answer = tokenizer.decode(input_ids[0][start_pos:end_pos+1])

            answers.append(answer)

        return answers
        
    def answer_question_single_context(self, question, text):
        # Implement the logic to use BERT for question answering on the relevant chunks
        # This implementation assumes you have a pretrained BERT model and tokenizer
        model = self.model
        tokenizer = self.tokenizer

        # Tokenize question and text as a pair
        encoded_input = tokenizer.encode_plus(question, text, add_special_tokens=True, max_length=512, truncation=True)
        input_ids = encoded_input['input_ids']
        token_type_ids = encoded_input['token_type_ids']
        
        # Model output using input_ids and token_type_ids
        output = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]))
        
        # Reconstruct the answer
        answer_start = torch.argmax(output.start_logits)
        answer_end = torch.argmax(output.end_logits)
        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        answer = ""
        
        if answer_end >= answer_start:
            answer = tokens[answer_start]
            for i in range(answer_start+1, answer_end+1):
                if tokens[i][0:2] == "##":
                    answer += tokens[i][2:]
                else:
                    answer += " " + tokens[i]
                    
        if answer.startswith("[CLS]"):
            answer = "Unable to find the answer to your question."
        
        return answer.capitalize()


    # def answer_question_single_context(self, question, text):
    #     # Implement the logic to use DistilBERT for question answering on the relevant chunks
    #     model = self.model
    #     tokenizer = self.tokenizer

    #     # Tokenize question and text as a pair
    #     encoded_input = tokenizer.encode_plus(question, text, add_special_tokens=True, max_length=512, truncation=True)
    #     input_ids = encoded_input['input_ids']
    #     attention_mask = encoded_input['attention_mask']

    #     # Model output using input_ids and attention_mask
    #     outputs = model(torch.tensor([input_ids]), attention_mask=torch.tensor([attention_mask]))
    #     start_scores = outputs.start_logits
    #     end_scores = outputs.end_logits

    #     # Reconstruct the answer
    #     answer_start = torch.argmax(start_scores)
    #     answer_end = torch.argmax(end_scores)

    #     tokens = tokenizer.convert_ids_to_tokens(input_ids)
    #     answer = ""

    #     if answer_end >= answer_start:
    #         answer = tokens[answer_start]
    #         for i in range(answer_start + 1, answer_end + 1):
    #             if tokens[i][0:2] == "##":
    #                 answer += tokens[i][2:]
    #             else:
    #                 answer += " " + tokens[i]

    #     if answer.startswith("[CLS]"):
    #         answer = "Unable to find the answer to your question."

    #     return answer.capitalize()

    #Transformer based approach
    def get_embedding(self, text):

        # Load the model
        tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
        model = AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')

        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy().squeeze()

    def find_most_relevant_text(self, question, texts):
        # Get the question embedding
        question_embedding = self.get_embedding(question)

        # Find the text with the smallest cosine distance to the question
        min_distance = 1.0
        most_relevant_text = None
        for text in texts:
            text_embedding = self.get_embedding(text)
            distance = cosine(question_embedding, text_embedding)
            if distance < min_distance:
                min_distance = distance
                most_relevant_text = text

        return most_relevant_text

    #TF-IDF based approach
    def find_most_relevant_text(self, question, texts):
        # Initialize the TfidfVectorizer
        vectorizer = TfidfVectorizer()

        # Train the vectorizer and transform the texts into vectors
        text_vectors = vectorizer.fit_transform(texts)

        # Transform the question into a vector
        question_vector = vectorizer.transform([question])

        # Compute the cosine similarity between the question and each text
        similarities = cosine_similarity(question_vector, text_vectors)

        # Get the index of the most similar text
        most_similar_index = similarities.argmax()

        return texts[most_similar_index]

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

    def preprocess_pdf(self, pdf_path, txt_path=None):
        
        '''
            Input: PDF book path
            Output: String of Processed txt from pdf, also saves as a txt file
            
            Process: 
                a) Remove Questions from the book (lines between . and ?)
        
        '''
        
        pdf_path = pdf_path.split("\\")[-1]
        if txt_path is None:
            txt_path = pdf_path.replace('.pdf', '.txt')

        print("Saving pdf converted to txt as: ", txt_path)
        extracted_text = self.convert_pdf_to_string(pdf_path, txt_path)
        
        print(len(extracted_text))
        
        processed_text = self.remove_substrings_with_dot_question(extracted_text)
        processed_text = self.remove_unicode_characters(processed_text)
        processed_text = self.remove_words_no_lowercase(processed_text)
        processed_text = self.remove_punctuation(processed_text)
        
        print(len(processed_text))
        
        output_path = 'D:/IntelliLearn Backend/processedBooks/'+txt_path
        print(output_path)
        # Write the extracted text to a text file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(processed_text)

        return output_path

    def answer_from_book(self, book_txt_path, question):

        answer_using = 1
        book = open(book_txt_path,encoding='utf-8').read()    
        book_text = book

        chunk_size = 400

        # Step 1: Splitting the book into chunks
        chunks = self.split_book_into_chunks(book_text, chunk_size)

        # Step 2: Indexing the chunks
        index = self.create_chunk_index(chunks)

        # Step 3: Preprocessing the question
        preprocessed_question = self.preprocess_question(question)

        # Step 4: Identifying relevant chunks
        relevant_chunks = self.find_relevant_chunks(preprocessed_question, index)

        # Step 5: Identifying topic boundaries
        topic_boundaries = self.identify_topic_boundaries(chunks)

        answer = ''
        if answer_using == 1: # bert-large-uncased-whole-word-masking-finetuned-squad
            # Step 6: Answering the question
            max_attempts = 7
            while answer == '' or answer == 'Unable to find the answer to your question.' or '[sep]' in answer:
                most_relevant_chunk = self.find_most_relevant_text(question, relevant_chunks)
                print(most_relevant_chunk)
                answer = self.answer_question_single_context(question, most_relevant_chunk)    

                relevant_chunks.pop(0) #try the next relevant chunk
                
                if len(relevant_chunks) == 0 or max_attempts == 0:
                    break
                max_attempts -= 1
                
            #answer = best_answer(question, relevant_chunks)
            print("Answer:", answer)
            print(len(answer))

        elif answer_using == 2:    #bert-base-uncased
            answer = self.answer_question(preprocessed_question, [most_relevant_chunk])
            print("Answer:", answer)

        return answer
    
    def answer_question_single_context_distilbert(self, question, text):

        model = self.model
        tokenizer = self.tokenizer

        # Tokenize question and text as a pair
        encoded_input = tokenizer.encode_plus(question, text, add_special_tokens=True, max_length=512, truncation=True)
        input_ids = encoded_input['input_ids']

        output = model(torch.tensor([input_ids]))

        # Reconstruct the answer
        answer_start = torch.argmax(output.start_logits)
        answer_end = torch.argmax(output.end_logits)
        tokens = tokenizer.convert_ids_to_tokens(input_ids)
        answer = ""

        if answer_end >= answer_start:
            answer = tokens[answer_start]
            for i in range(answer_start+1, answer_end+1):
                if tokens[i][0:2] == "##":
                    answer += tokens[i][2:]
                else:
                    answer += " " + tokens[i]

        if answer.startswith("[CLS]"):
            answer = "Unable to find the answer to your question."
        
        # Return answer and start and end probabilities
        return answer.capitalize(), output.start_logits[0, answer_start].item(), output.end_logits[0, answer_end].item()

    def answer_from_book_using_distilbert(self, book_txt_path, question):

        answer_using = 1
        book = open(book_txt_path,encoding='utf-8').read()    
        book_text = book

        chunk_size = 400

        # Step 1: Splitting the book into chunks
        chunks = self.split_book_into_chunks(book_text, chunk_size)

        # Step 2: Indexing the chunks
        index = self.create_chunk_index(chunks)

        # Step 3: Preprocessing the question
        preprocessed_question = self.preprocess_question(question)

        # Step 4: Identifying relevant chunks
        relevant_chunks = self.find_relevant_chunks(preprocessed_question, index)

        # Step 5: Identifying topic boundaries
        topic_boundaries = self.identify_topic_boundaries(chunks)

        answer = ''

        if answer_using == 1: 
            max_attempts = min(7, len(relevant_chunks))  # Modify to get min of 7 and length of relevant chunks
            best_answer = None
            max_start_prob = float('-inf')
            max_end_prob = float('-inf')

            for _ in range(max_attempts):
                most_relevant_chunk = self.find_most_relevant_text(question, relevant_chunks)
                print(most_relevant_chunk)
                answer, start_prob, end_prob = self.answer_question_single_context_distilbert(question, most_relevant_chunk)    
                print("\n\n\nANSWER:", answer)
                if start_prob + end_prob > max_start_prob + max_end_prob and len(answer) > 2:

                    best_answer = answer
                    max_start_prob = start_prob
                    max_end_prob = end_prob

                relevant_chunks.pop(0)

            print("Answer:", best_answer)
            print(len(best_answer))

        elif answer_using == 2:    
            answer = self.answer_question(preprocessed_question, [most_relevant_chunk])
            print("Answer:", answer)

        return best_answer if best_answer is not None else answer
