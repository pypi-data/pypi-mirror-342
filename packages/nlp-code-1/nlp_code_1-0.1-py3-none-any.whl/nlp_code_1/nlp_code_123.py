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