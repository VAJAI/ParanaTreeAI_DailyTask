'''Tokenization'''
# from nltk.tokenize import word_tokenize

# text ="Hello this ajai know i am sad because of my ??"
# tokens = word_tokenize(text)
# print("Word-tokens :",tokens)


'''Stemming'''

# from nltk.stem import PorterStemmer
# stemmer = PorterStemmer()

# words = ["running", "runner", "ran", "easily", "fairly"]
# stems =[stemmer.stem(word) for word in words]
# print(stems) 


'''Lematization''' 

# from nltk.stem import WordNetLemmatizer

# lemmatizer = WordNetLemmatizer()
# words = ["running", "better", "plays", "geese","happy"]

# lemmas = [lemmatizer.lemmatize(word,pos='a') for word in words]
# print("Lemmatized Words:", lemmas)


'''StopWords'''
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords

# text= "Hello this is ajai how are you guys"
# tokens=word_tokenize(text)
# stop_words = set(stopwords.words('english'))

# filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
# print("Tokens after Removing Stop Words:", filtered_tokens)

'''TextBlog'''
# from textblob import TextBlob
# text = "I love programming. It's amazing and exciting!"
# blog = TextBlob(text)
# result= blog.sentiment
# print("Polarity :",result.polarity,"Subjectivity : ",result.subjectivity)

'''Project Task'''

# from textblob import TextBlob

# def sentiment_anlysis(user_input):
#     blog =TextBlob(user_input)
#     sentiment =blog.sentiment.polarity
    
#     if sentiment > 0:
#         feedback = "Positive Sentiment"
#     elif sentiment < 0:
#         feedback = "Negative Sentiment"
#     else:
#         feedback = "Netural Sentiment"
    
#     return sentiment,feedback

# user_input = input("Enter a Sentence : ")

# sentiment,feedback = sentiment_anlysis(user_input)
# print("Sentiment Score : ",{sentiment})
# print(feedback)