import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai



genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to analyze question paper patterns using Gemini
def analyze_patterns_with_gemini(text):
    prompt = f"""
    You are a system trained to analyze educational question papers. 
    Analyze the structure and pattern of the provided question papers. 
    Identify details such as:
    - Total number of questions.
    - Types of questions (e.g., short answers, long answers, multiple-choice, etc.).
    - Marks distribution.
    - Any noticeable sections or patterns (e.g., grouped by topic).
    Provide your analysis in a structured format.
    Question Paper Text:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to generate a new question paper using the identified pattern
def generate_question_paper_with_pattern(text, pattern_analysis):
    prompt = f"""
    You are a system trained to create educational question papers. 
    Based on the following pattern analysis, generate a new question paper that follows the same structure and distribution:
    Pattern Analysis:
    {pattern_analysis}
    Use the content provided in the uploaded question papers as a source. Create a new question paper with the same pattern.
    Question Paper Text:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Initialize session state variables
if "pattern_analysis" not in st.session_state:
    st.session_state.pattern_analysis = None

if "new_question_paper" not in st.session_state:
    st.session_state.new_question_paper = None

if "combined_text" not in st.session_state:
    st.session_state.combined_text = None

# Streamlit App
st.title("Gemini-Powered Question Paper Generator")

# File uploader
uploaded_files = st.file_uploader("Upload Question Papers (PDF only)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    # Extract text from uploaded files
    all_text = []
    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        all_text.append(text)
    st.session_state.combined_text = " ".join(all_text)

    st.success("Files uploaded successfully!")

    # Analyze patterns
    if st.button("Analyze Patterns"):
        st.session_state.pattern_analysis = analyze_patterns_with_gemini(st.session_state.combined_text)
        st.subheader("Pattern Analysis")
        st.write(st.session_state.pattern_analysis)

# Generate new question paper
if st.session_state.pattern_analysis and st.button("Generate Question Paper"):
    st.session_state.new_question_paper = generate_question_paper_with_pattern(
        st.session_state.combined_text, st.session_state.pattern_analysis
    )
    st.subheader("Generated Question Paper")
    st.write(st.session_state.new_question_paper)

    # Option to download
    st.download_button(
        label="Download Question Paper",
        data=st.session_state.new_question_paper,
        file_name="generated_question_paper.txt"
    )
