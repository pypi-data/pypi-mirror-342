def ex1():
    print("""
#python -m spacy download en_core_web_sm

import PyPDF2
import spacy
import pandas as pd

# Load the spaCy language model
nlp = spacy.load('en_core_web_sm')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to screen resume for keyword matches
def screen_resume(text, keywords):
    doc = nlp(text.lower())
    matches = {keyword: 0 for keyword in keywords}
    for token in doc:
        if token.text in matches:
            matches[token.text] += 1
    return matches

# Function to accept or reject resume based on keyword frequency
def accept_resume(matches, threshold=1):
    return all(count >= threshold for count in matches.values())

# List of keywords to search
keywords = ['python', 'data', 'cluny']

# Path to the resume PDF
pdf_path = r"C:\\Users\\gokulan\\Pictures\\Resume_Gokulan.pdf"

# Resume screening process
resume_text = extract_text_from_pdf(pdf_path)
keyword_matches = screen_resume(resume_text, keywords)
is_accepted = accept_resume(keyword_matches, threshold=1)

# Display results
df = pd.DataFrame(keyword_matches.items(), columns=['Keyword', 'Count'])
print(df)
print("Resume Accepted" if is_accepted else "Resume Rejected")
          """)
    
def ex2():
    print("""
        import spacy

# Function to perform Named Entity Recognition
def perform_ner(text):
    nlp = spacy.load('en_core_web_sm')  # Load spaCy English model
    doc = nlp(text)  # Process the text
    return [(ent.text, ent.label_) for ent in doc.ents]  # Extract entities

# Main function
def main():
    sample_text = "Mark Zuckerberg is one of the founders of Facebook, a company from the United States."
    ner_results = perform_ner(sample_text)
    
    print("Named Entities and Labels:")
    for entity, label in ner_results:
        print(f"Entity: {entity}, Label: {label}")

if __name__ == "__main__":
    main()
  """
          )
    
def ex3():
    print("""
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download the VADER sentiment lexicon (only needed once)
nltk.download('vader_lexicon')

# Function to perform sentiment analysis
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)['compound']
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Example texts
texts = [
    "I enjoyed the movie. It was a great experience.",
    "How are you"
]

# Analyze and print sentiment for each text
for text in texts:
    sentiment = analyze_sentiment(text)
    print(f"Text: {text}\\nSentiment: {sentiment}\\n")

          """)
    
def ex4():
    print("""
import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Function to extract keywords
def extract_keywords(text):
    #"Extract keywords from the given text using spaCy."
    doc = nlp(text)
    keywords = set()

    # Add named entities and noun chunks to the keyword set
    for entity in doc.ents:
        keywords.add(entity.text)
    for chunk in doc.noun_chunks:
        keywords.add(chunk.text)

    return list(keywords)

# Main execution
def main():
    example_text = "Natural language processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans using natural language. It involves the development of algorithms and models that enable computers to understand, interpret, and generate human-like language."

    keywords = extract_keywords(example_text)
    print("Extracted Keywords:")
    for kw in keywords:
        print("-", kw)

if __name__ == "__main__":
    main()
          
""")
    
def ex5():
    print("""
from spellchecker import SpellChecker

# Function to correct spelling in the input text
def correct_spelling(text):
    spell = SpellChecker()
    words = text.split()
    corrected_words = [spell.correction(word) for word in words]
    corrected_sentence = ' '.join(corrected_words)
    return corrected_sentence

# Main block
def main():
    sample_text = "Thiss is an examplee sentence with somme spellling mistakkes."
    corrected = correct_spelling(sample_text)
    
    print("Original text: ", sample_text)
    print("Corrected text:", corrected)

if __name__ == "__main__":
    main()

""")
    
def ex6():
    print("""
from difflib import get_close_matches

# Function to build the autocorrect model
def build_autocorrect_model(words):
    return {word.lower(): word for word in words}

# Function to autocorrect input text
def autocorrect_input(input_text, autocorrect_model):
    corrected_text = []
    for word in input_text.split():
        corrected_word = autocorrect_model.get(word.lower())
        if corrected_word:
            corrected_text.append(corrected_word)
        else:
            closest_match = get_close_matches(word.lower(), autocorrect_model.keys(), n=1, cutoff=0.8)
            if closest_match:
                corrected_text.append(autocorrect_model[closest_match[0]])
            else:
                corrected_text.append(word)
    return ' '.join(corrected_text)

# Main function
def main():
    word_list = ['apple', 'banana', 'cat', 'dog', 'elephant', 'fish']
    model = build_autocorrect_model(word_list)
    input_text = "I like to eat applle and bananana."
    corrected = autocorrect_input(input_text, model)
    print("Original text: ", input_text)
    print("Corrected text:", corrected)

if __name__ == "__main__":
    main()

""")
    
def ex7():
    print("""
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer

# Sample data: tweets with sentiment (1 = positive, 0 = negative)
tweets = [
    ("I hate candidate A", 0),
    ("I love candidate B", 1),
    ("Candidate A is terrible", 0),
    ("I support candidate B", 1),
    ("Can't stand candidate A", 0),
    ("I'm voting for candidate B", 1)
]

# Preprocessing function
tokenizer = TreebankWordTokenizer()
def preprocess(text):
    text = re.sub(r'[^a-zA-Z\\s]', '', text.lower())
    words = tokenizer.tokenize(text)
    return ' '.join([w for w in words if w not in stopwords.words('english')])

# Data preparation
df = pd.DataFrame(tweets, columns=['text', 'sentiment'])
df['clean_text'] = df['text'].apply(preprocess)
X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['sentiment'], test_size=0.2, random_state=42)

# Vectorization and Model
vectorizer = TfidfVectorizer(max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_vec, y_train)
y_pred = model.predict(X_test_vec)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Sentiment analysis per candidate
sentiment_df = pd.DataFrame({'text': X_test, 'predicted': y_pred})
sentiment_df['candidate'] = sentiment_df['text'].apply(lambda x: 'A' if 'candidate a' in x.lower() else ('B' if 'candidate b' in x.lower() else None))
avg_sentiment = sentiment_df.groupby('candidate')['predicted'].mean()
winner = avg_sentiment.idxmax()

print(f"Candidate {winner} has the highest possibility of winning.")

""")
    
def ex8():
    print("""
import spacy
from textblob import TextBlob

nlp = spacy.load("es_core_news_sm")
text = "Me encanta la comida mexicana y el tequila."
doc = nlp(text)
print("\nTokens and POS tags:")
for token in doc:
    print(token.text, token.pos_)
print("\\nNamed Entities:")
for ent in doc.ents:
    print(ent.text, ent.label_)
sentiment_score = 0
for sentence in doc.sents:
    analysis = TextBlob(sentence.text)
    sentiment_score += analysis.sentiment.polarity
print("\\nSentiment score:", sentiment_score)

""")

def ex9():
    print("""
from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the dataset
(X_train, y_train), _ = imdb.load_data(num_words=10000)
X_train = pad_sequences(X_train, maxlen=100)

# Build the model
model = Sequential([
    Embedding(10000, 32),
    LSTM(32),
    Dense(1, activation="sigmoid")
])

# Compile and train
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=1, batch_size=64)

""")
    
def ex10():
    print("""
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

text = input('Enter text to summarize: ')
parser = PlaintextParser.from_string(text, Tokenizer('english'))
summarizer = LsaSummarizer()

summary = summarizer(parser.document, 2)

for sentence in summary:
    print(sentence)

""")
    
def chat():
    print("""

import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Symptom-to-disease mapping
symptom_disease_mapping = {
    "fever": ["flu", "malaria", "COVID-19"],
    "cough": ["common cold", "flu", "pneumonia"],
    "headache": ["migraine", "tension headache", "sinusitis"]
}

# Preprocessing function
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stopwords.words("english")]
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(t) for t in tokens]

# Diagnosis function
def consult_health_system(symptoms):
    tokens = preprocess_text(" ".join(symptoms))
    for symptom in tokens:
        if symptom in symptom_disease_mapping:
            return f"You might have {random.choice(symptom_disease_mapping[symptom])}."
    return "Could not determine a specific disease. Please consult a doctor."

# Example usage
user_symptoms = ["fever", "cough"]
print(consult_health_system(user_symptoms))

          """)