def resume_screening():
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
    
def named_entity():
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
    
def Sentiment():
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
    print(f"Text: {text}\nSentiment: {sentiment}\n")

          """)
    
def keywordExtract():
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
    
def spellingcheck():
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
    
def autocorrect():
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
    
def election():
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
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
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
    
def multilingual():
    print("""
import spacy
from textblob import TextBlob

nlp = spacy.load("es_core_news_sm")
text = "Me encanta la comida mexicana y el tequila."
doc = nlp(text)
print("\nTokens and POS tags:")
for token in doc:
    print(token.text, token.pos_)
print("\nNamed Entities:")
for ent in doc.ents:
    print(ent.text, ent.label_)
sentiment_score = 0
for sentence in doc.sents:
    analysis = TextBlob(sentence.text)
    sentiment_score += analysis.sentiment.polarity
print("\nSentiment score:", sentiment_score)

""")

def deeplerning():
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
    
def summarization():
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
    
def chatbot1():
    print("""

from nltk.chat.util import Chat, reflections

# List of patterns and responses
chat_data = [
    [r"hi|hello|hey", ["Hello! How can I help you today?"]],
    [r"what is your name?", ["I'm your chatbot. You can give me any name you like!"]],
    [r"i want help with (.*)", ["Sure, I can help you with %1. Please tell me more."]],
    [r"(.*) your location", ["I'm a virtual assistant, but I can help you find places if you need."]],
    [r"thank you|thanks", ["You're welcome!", "Glad to help!"]],
    [r"(.*)", ["Sorry, I didn’t understand that. Can you ask in a different way?"]],
]

# Create chatbot
chatbot = Chat(chat_data, reflections)

print("Welcome! I'm your chatbot. Type 'bye', 'exit', or 'quit' to end.")

while True:
    user_input = input("You: ").lower()
    if user_input in ["bye", "exit", "quit"]:
        print("Bot: Goodbye! Have a great day!")
        break
    else:
        response = chatbot.respond(user_input)
        print("Bot:", response)

          """)
def answercheck():
    print("""

import nltk
from nltk.metrics import jaccard_distance

def get_tokens(text):
    tokens = text.split()
    tokens = [token.lower() for token in tokens]
    return tokens

def calculate_similarity(answer, correct_answer):
    answer_set = set(get_tokens(answer))
    correct_answer_set = set(get_tokens(correct_answer))
    similarity = 1 - jaccard_distance(answer_set, correct_answer_set)
    return similarity

def check_answer(answer, correct_answer):
    similarity = calculate_similarity(answer, correct_answer)
    similarityArray.append(similarity)
    return similarity != 0

# 👇 Replace with fingerprint-related questions
Questions = {
    "1": "What is the unique pattern used to identify a person in fingerprint biometrics?",
    "2": "Which layer of skin forms the fingerprint pattern?",
    "3": "What is the name of the loop, whorl, and arch in fingerprint types?",
    "4": "Which chemical is often used to reveal latent fingerprints?",
    "5": "What is the term for an unintentional print left on a surface?"
}

CorrectAnswer = {
    "1": "Ridge pattern",
    "2": "Dermis",
    "3": "Fingerprint patterns",
    "4": "Ninhydrin",
    "5": "Latent fingerprint"
}

UserAnswer = {}
similarityArray = []
CountofQuestions = len(Questions)

# Take input from the user
for i in range(1, CountofQuestions + 1):
    question = Questions.get(str(i))
    user_input = input(f"{question}\nYour answer: ")
    UserAnswer[str(i)] = user_input

# Check answers
for i in range(1, CountofQuestions + 1):
    check_answer(UserAnswer.get(str(i)), CorrectAnswer.get(str(i)))

total_score = round(sum(similarityArray), 2)
print(f"\nYour score is {total_score} out of {CountofQuestions}")
""")
    
def plagrism():
    print("""
from collections import Counter
import math

def get_words(text):
    words = text.lower().split()
    return Counter(words)

def cosine_similarity(counter1, counter2):
    all_words = set(counter1.keys()).union(set(counter2.keys()))
    vec1 = [counter1.get(word, 0) for word in all_words]
    vec2 = [counter2.get(word, 0) for word in all_words]
    
    dot_product = sum(i * j for i, j in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(i ** 2 for i in vec1))
    magnitude2 = math.sqrt(sum(j ** 2 for j in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def main():
    file1 = input("Enter path of the first text file: ")
    file2 = input("Enter path of the second text file: ")
    
    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            text1 = f1.read()
        with open(file2, 'r', encoding='utf-8') as f2:
            text2 = f2.read()

        counter1 = get_words(text1)
        counter2 = get_words(text2)
        similarity = cosine_similarity(counter1, counter2)
        percentage = round(similarity * 100, 2)
        print(f"\nPlagiarism Match: {percentage}%")

    except FileNotFoundError:
        print("One or both file paths are invalid. Please check and try again.")

if __name__ == "__main__":
    main()


""")
    
def appti():
    print("""
import random

# Simple in-memory "database" for users
users = {}

# Sample questions
questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Berlin', 'Rome'],
        'answer': 'Paris'
    },
    {
        'question': 'Which is the largest planet in our solar system?',
        'options': ['Jupiter', 'Saturn', 'Mars', 'Earth'],
        'answer': 'Jupiter'
    },
    {
        'question': 'What is the square root of 64?',
        'options': ['4', '6', '8', '10'],
        'answer': '8'
    },
]

# Function to register users
def register_user():
    print("Register a new user")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users:
        print("Username already exists. Try logging in.")
    else:
        users[username] = password
        print("Registration successful! You can now log in.")

# Function to log in
def login_user():
    print("Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username] == password:
        print(f"Welcome back, {username}!")
        return username
    else:
        print("Invalid username or password. Try again.")
        return None

# Function to ask a question
def ask_question(question):
    print("\n" + question['question'])
    for i, option in enumerate(question['options']):
        print(f'{i + 1}. {option}')
    user_answer = input('Enter the answer (text only): ').strip()
    return user_answer

# Function to evaluate answers
def evaluate_answers(answers, correct_answers):
    score = 0
    for user_ans, correct_ans in zip(answers, correct_answers):
        if user_ans.lower() == correct_ans.lower():
            score += 1
    return score

# Function to run the aptitude test
def run_aptitude_test(username):
    print("\nStarting the Aptitude Test!\nAnswer the following questions:")
    random.shuffle(questions)
    user_answers = []
    correct_answers = []
    for question in questions:
        user_answer = ask_question(question)
        user_answers.append(user_answer)
        correct_answers.append(question['answer'])
    score = evaluate_answers(user_answers, correct_answers)
    total_questions = len(questions)
    percentage = (score / total_questions) * 100
    print("\n----- Results -----")
    print(f"You scored {score} out of {total_questions}")
    print(f"Percentage: {percentage:.2f}%")
    print(f"Thank you for taking the test, {username}!")

# Main function
def main():
    print("Welcome to the Aptitude Test System!")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register_user()
        elif choice == '2':
            username = login_user()
            if username:
                run_aptitude_test(username)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()


""")
    
def shop():
    print("""
          
import random

products = {
    "laptop": {"price": 60000, "description": "14-inch laptop with 8GB RAM and 512GB SSD"},
    "phone": {"price": 30000, "description": "Smartphone with 6.5-inch display and 128GB storage"},
    "headphones": {"price": 2000, "description": "Wireless headphones with noise cancellation"},
    "watch": {"price": 5000, "description": "Smartwatch with heart rate monitor"},
    "camera": {"price": 25000, "description": "DSLR camera with 24MP sensor and 4K video"}
}

cart = {}

def recommend_products():
    print("\nRecommended for you:")
    for item in random.sample(list(products), 3):
        print(f"- {item.capitalize()}: ₹{products[item]['price']}")

def show_products():
    print("\nAvailable Products:")
    for name, details in products.items():
        print(f"- {name.capitalize()}: ₹{details['price']} ({details['description']})")

def add_to_cart(product_name):
    if product_name in products:
        cart[product_name] = cart.get(product_name, 0) + 1
        print(f"✅ {product_name.capitalize()} added to your cart.")
    else:
        print("❌ Product not found.")

def view_cart():
    if not cart:
        print("🛒 Your cart is empty.")
        return
    print("\n🛒 Your Cart:")
    total = 0
    for item, qty in cart.items():
        price = products[item]['price'] * qty
        print(f"- {item.capitalize()} x{qty} = ₹{price}")
        total += price
    print(f"💰 Total: ₹{total}")

def checkout():
    if not cart:
        print("🛒 Your cart is empty. Add items before checking out.")
        return
    view_cart()
    print("✅ Checkout complete. Thank you for shopping with us!")

def assistant():
    print("👋 Welcome to AI Shopping Assistant!")
    recommend_products()
    while True:
        print("\nType: 'show' to view products, 'add [product]', 'cart', 'checkout', or 'exit'")
        user_input = input("You: ").lower()
        if user_input == "show":
            show_products()
        elif user_input.startswith("add "):
            product_name = user_input.replace("add ", "").strip()
            add_to_cart(product_name)
        elif user_input == "cart":
            view_cart()
        elif user_input == "checkout":
            checkout()
            break
        elif user_input == "exit":
            print("👋 Goodbye!")
            break
        else:
            print("❓ I didn't understand that. Try again.")

# Run the assistant
assistant()



""")
    
def tourism():
    print("""
import json

class TourismAssistant:
    def __init__(self):
        self.destinations = []

    def load_destinations_from_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.destinations = json.load(file)

    def get_destination(self, city_name):
        print(f"\nDetails for '{city_name.capitalize()}':\n")
        found = False
        for destination in self.destinations:
            if destination['name'].lower() == city_name.lower():
                found = True
                print(f"• {destination['name']} - {destination['location']}")
                print(f"  Rating: {destination['rating']}")
                print(f"  Description: {destination['description']}")
                print(f"  Temperature: {destination['temperature']}")
                print("  Nearby Hotels:")
                for hotel in destination['hotels']:
                    print(f"   - {hotel}")
                break
        if not found:
            print("City not found in our travel guide. Please try another.")

# --- Main Program ---
if __name__ == '__main__':
    assistant = TourismAssistant()
    assistant.load_destinations_from_json('newtext.json')  # JSON file should exist
    user_input = input("Enter a city name (e.g., Paris, London): ")
    assistant.get_destination(user_input)
#############################################################################################
          [
    {
        "name": "Paris",
        "location": "France",
        "rating": "4.9",
        "type": "city",
        "description": "The city of lights and love.",
        "temperature": "16°C",
        "hotels": ["Hotel Le Meurice", "Hotel Lutetia", "Shangri-La Hotel"]
    },
    {
        "name": "London",
        "location": "United Kingdom",
        "rating": "4.8",
        "type": "city",
        "description": "Capital of England, rich in history and culture.",
        "temperature": "14°C",
        "hotels": ["The Savoy", "Claridge's", "The Ritz London"]
    }
]


    


""")
    
def teachtime():
    print("""
import random

# Step 1: Define classes for Teacher and Subject
class Teacher:
    def __init__(self, name):
        self.name = name

class Subject:
    def __init__(self, name, teacher):
        self.name = name
        self.teacher = teacher

# Step 3: Function to generate time table
def generate_time_table(subjects, classrooms):
    timetable = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods = ["9AM-10AM", "10AM-11AM", "11AM-12PM", "1PM-2PM", "2PM-3PM"]

    for day in days:
        timetable[day] = []
        available_classrooms = classrooms.copy()

        for period in periods:
            if not subjects or not available_classrooms:
                timetable[day].append((period, "Free Period", "No Room"))
                continue

            subject = random.choice(subjects)
            classroom = random.choice(available_classrooms)
            available_classrooms.remove(classroom)

            timetable[day].append((period, subject.name, subject.teacher.name, classroom))
    
    return timetable

# Step 4: Main function
def main():
    # Step 2: Prompt user for input
    num = int(input("Enter number of subjects: "))
    subjects = []

    for _ in range(num):
        teacher_name = input("Enter teacher name: ")
        subject_name = input("Enter subject name: ")
        teacher = Teacher(teacher_name)
        subject = Subject(subject_name, teacher)
        subjects.append(subject)

    classrooms = input("Enter available classrooms (comma-separated): ").split(",")

    timetable = generate_time_table(subjects, classrooms)

    # Display the timetable
    print("\nGenerated Timetable:")
    for day, schedule in timetable.items():
        print(f"\n{day}")
        for entry in schedule:
            if len(entry) == 3:
                period, subj, room = entry
                print(f"{period} - {subj} in {room}")
            else:
                period, subj, teacher, room = entry
                print(f"{period} - {subj} by {teacher} in {room}")

if __name__ == "__main__":
    main()


""")
    
def attendance():
    print(""""
import datetime
import os
import cv2

# Simulated database of retina images and student IDs
retina_database = {
    "retina1.jpg": 101,
    "retina2.jpg": 102,
    "retina3.jpg": 103
}

# Attendance record dictionary
student_records = {}

def simulate_retina_match(input_image_path):
    # Simulate retina match by filename comparison (demo purpose)
    filename = os.path.basename(input_image_path)
    return retina_database.get(filename, None)

def mark_attendance(student_id):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if student_id not in student_records:
        student_records[student_id] = now
        return f"✅ Attendance marked for student ID {student_id} at {now}"
    else:
        return f"⚠ Already marked for student ID {student_id} at {student_records[student_id]}"

def view_attendance():
    if not student_records:
        return "📭 No attendance records."
    return "\n".join([f"ID: {sid}, Time: {time}" for sid, time in student_records.items()])

def main():
    print("👁 Retina-Based Attendance System")
    print("Place retina image (e.g., 'retina1.jpg') or type 'view' or 'exit'\n")

    while True:
        user_input = input("Retina image path or command: ").strip()
        if user_input.lower() == "exit":
            print("👋 Exiting system.")
            break
        elif user_input.lower() == "view":
            print(view_attendance())
        elif os.path.exists(user_input):
            student_id = simulate_retina_match(user_input)
            if student_id:
                print(mark_attendance(student_id))
            else:
                print("❌ Retina not recognized.")
        else:
            print("⚠ File not found or invalid input.")

if __name__ == "__main__":
    main()

  
""")