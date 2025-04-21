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
    
def answercheck():
    print("""

similarityArray=[] 
Questions = {
"1": "What is part of a database that holds only one type of information?", 
"2": "'OS' computer abbreviation usually means?",
"3": "What was the active medium used in the first working laser ever constructed?",
"4": "'.MOV' extension refers usually to what kind of file?", 
"5": "What does EPROM stand for?"
}

CorrectAnswer = { "1": "Field",
"2": "Operating System",
"3": "A ruby rod",
"4": "Animation movie file",
"5": "Erasable Programmable Read Only Memory"
}
UserAnswer = { "1": "Field",
"2": "Operation Subset",
"3": "Titanium",
"4": "Animation",
"5": "Erasable Programmable Read Only Memory"
}

CountofQuestions = 5

def check_answer(a,b):
    tokens=a.split()
    tokensa=[token.lower() for token in tokens]
    tokens=b.split()
    tokensb=[token.lower() for token in tokens]
    answer_set=set(tokensa)
    Correct_set=set(tokensb)
    similarity=1-nltk.jaccard_distance(answer_set,Correct_set)
    similarityArray.append(similarity)
    
for i in range(1, CountofQuestions+1): 
    check_answer(UserAnswer.get(str(i)), CorrectAnswer.get(str(i)))

print(f"Your score is {sum(similarityArray)}")
""")
    
def plagrism():
    print("""
from difflib import SequenceMatcher
while True:
    user_input=input("Enter the passage")
    if user_input=="q":
        break
    check_ans=input("Compare data kudu")
    similarty=SequenceMatcher(None,user_input,check_ans).ratio()
    print(similarty)
""")
    
def appti():
    print("""
def run_aptitude_test():
    import random

    # Define the questions
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

    print("🧠 Welcome to the Aptitude Test Chatbot!\nAnswer the following questions:\n")

    random.shuffle(questions)  # Randomize questions
    score = 0

    for q in questions:
        print(q['question'])
        for i,option in enumerate(q['options'], 1):
            print(f"{i}. {option}")
        user_answer = input("Enter your answer (text only): ").strip()

        if user_answer.lower() == q['answer'].lower():
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. Correct answer: {q['answer']}\n")

    total = len(questions)
    percentage = (score / total) * 100

    print("📊 ----- Results -----")
    print(f"Score: {score} out of {total}")
    print(f"Percentage: {percentage:.2f}%")

# Run the chatbot
run_aptitude_test()

""")
    
def shop():
    print("""
available_prod={"smartphone":500,
                "brush":600,
                "bottle":700,
                "lays":800,
                "perk":300}
wallet_bal=1500
shop_cart=[]
for product,price in available_prod.items():
    print(f"product:{product} price:{price}")
while True:
    user_input=input("Enter the required prod")
    if user_input.lower()=="q":
        break
    if user_input in available_prod:
        shop_cart.append(user_input)
    
    else:
        print("Irukardha sollu da")
total=sum([available_prod[product] for product in shop_cart])
if total>wallet_bal:
    print("insufficient balance")
else:
    print("purchase succesful ")
    wallet_bal=wallet_bal-total
print(f"balance:{wallet_bal}")

""")
    
def tourism():
    print("""
def get_location_info(location):
    locations = {
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Tokyo": (35.6895, 139.6917),
    }
    return locations.get(location)
def find_nearby_attractions(location): 
    attractions = {
"New York": ["Statue of Liberty", "Central Park", "Empire State Building"],
"London": ["Big Ben", "Tower of London", "British Museum"], "Paris": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"],
"Tokyo": ["Tokyo Tower", "Senso-ji Temple", "Shinjuku Gyoen National Garden"], }
    return attractions.get(location, [])

def find_nearby_restaurants(location): 
    restaurants = {
"New York": ["Joe's Pizza", "Shake Shack", "Katz's Delicatessen"], "London": ["Dishoom", "Sketch", "The Wolseley"],
"Paris": ["Le Comptoir du Relais", "La Tour d'Argent", "L'Ambroisie"], "Tokyo": ["Sushi Dai", "Ichiran Ramen", "Ginza Kojyu"],
    }
    return restaurants.get(location, [])

def get_weather_info(location):
    weather = {
"New York": {"temperature": "30°C", "description": "Sunny"}, "London": {"temperature": "20°C", "description": "Partly Cloudy"}, "Paris": {"temperature": "25°C", "description": "Clear Sky"},
"Tokyo": {"temperature": "28°C", "description": "Cloudy"},
    }
    return weather.get(location, {})

if __name__== "__main__":
    while True:
    location = input("Enter the desired location (or 'q' to quit): ") if location.lower() == 'q':
    print("Exiting the program.") break
    location_info = get_location_info(location)
    if location_info:
        latitude, longitude = location_info print("Latitude:", latitude) print("Longitude:", longitude)
        nearby_attractions = find_nearby_attractions(location) print("Nearby attractions:", ", ".join(nearby_attractions) if
        nearby_attractions else "No attractions found.")
        nearby_restaurants = find_nearby_restaurants(location) print("Nearby restaurants:", ", ".join(nearby_restaurants) if
        nearby_restaurants else "No restaurants found.")

        weather_info = get_weather_info(location)
        print("Weather Information:")
        print("Temperature:", weather_info.get('temperature', "N/A"))
        print("Description:", weather_info.get('description', "N/A"))
    else:
        print("Location not found.")
""")
    
def teachtime():
    print("""
teachers = {
"Alice": ["Math", "Science"],
"Bob": ["English", "History"],
"Carol": ["Math", "Geography"],
"David": ["Science", "Physics"],
}
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
timings = ["9 AM", "10 AM", "11 AM", "2 PM", "3 PM"]
import random
def generate_timetable(): 
    timetable = {}
    for day in days: 
        timetable[day] = {}
        for timing in timings:
            teacher = random.choice(list(teachers.keys()))
            subject = random.choice(teachers[teacher])
            timetable[day][timing] = {"teacher": teacher, "subject": subject}
    return timetable
def print_timetable(timetable):
    for day in days: 
        print(f"\\\\n{day}:")
            for timing in timings:
                class_info = timetable[day][timing]
                print(f"{timing} - {class_info['teacher']} - {class_info['subject']}")
def main():
    print("Welcome to the Teacher's Automatic Timetable Software!") print("Generating Timetable...\\\\n")
    timetable = generate_timetable()
    print_timetable(timetable)
    main()
""")
    
def attendance():
    print(""""
import datetime

student_records = {}

def mark_attendance(student_id):
    now = datetime.datetime.now()
    if student_id not in student_records:
        student_records[student_id] = now
        return f"Attendance marked for ID {student_id} at {now}"
    return f"Attendance already marked at {student_records[student_id]}"

def view_attendance():
    return "No attendance records found." if not student_records else "\n".join([
        f"ID: {sid}, Time: {time.strftime('%Y-%m-%d %H:%M:%S')}" for sid, time in student_records.items()
    ])

print("\n[Experiment 10] Attendance System:")
print(mark_attendance(101))
print(mark_attendance(102))
print(mark_attendance(101))
print("\nAttendance Records:")
print(view_attendance())  
""")