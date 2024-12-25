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

# Function to generate answers for Mathematics questions
def generate_math_answers_with_gemini(text):
    prompt = f"""
    You are an advanced educational assistant trained to generate answers. 
    Extract and provide answers only for the Mathematics-related questions from the following question paper:
    Question Paper Text:
    {text}
    Provide detailed and accurate solutions.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Multi-page app structure
st.sidebar.title("Question Paper Tools")
app_mode = st.sidebar.selectbox("Choose an option", ["Generate Question Paper", "Generate Answers"])

# Generate Question Paper Page
if app_mode == "Generate Question Paper":
    st.title("Gemini-Powered Question Paper Generator")

    # File uploader
    uploaded_files = st.file_uploader("Upload Question Papers (PDF only)", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        # Extract text from uploaded files
        all_text = []
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            all_text.append(text)
        combined_text = " ".join(all_text)

        st.success("Files uploaded successfully!")

        # Analyze patterns
        if st.button("Analyze Patterns"):
            pattern_analysis = analyze_patterns_with_gemini(combined_text)
            st.subheader("Pattern Analysis")
            st.write(pattern_analysis)

            # Generate new question paper
            if st.button("Generate Question Paper"):
                new_question_paper = generate_question_paper_with_pattern(combined_text, pattern_analysis)
                st.subheader("Generated Question Paper")
                st.write(new_question_paper)

                # Option to download
                st.download_button(
                    label="Download Question Paper",
                    data=new_question_paper,
                    file_name="generated_question_paper.txt"
                )

# Generate Answers Page
elif app_mode == "Generate Answers":
    st.title("Gemini-Powered Answer Generator")

    # File uploader
    uploaded_file = st.file_uploader("Upload Question Paper (PDF only)", type=["pdf"])

    if uploaded_file:
        # Extract text from the uploaded file
        question_paper_text = extract_text_from_pdf(uploaded_file)
        st.success("File uploaded successfully!")

        # Generate answers for Mathematics section
        if st.button("Generate Answers"):
            math_answers = generate_math_answers_with_gemini(question_paper_text)
            st.subheader("Generated Answers (Mathematics)")
            st.write(math_answers)

            # Option to download
            st.download_button(
                label="Download Answers",
                data=math_answers,
                file_name="math_answers.txt"
            )
