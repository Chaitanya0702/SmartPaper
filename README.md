# **Gemini-Powered Question Paper Generator**

## **Description**
This Streamlit app allows you to upload previous question papers (in PDF format), analyze their patterns using the **Gemini API**, and generate new question papers that follow the same structure and distribution of questions.

The app uses the **Gemini 1.5 Pro LLM** to:
1. Analyze the structure of the uploaded question papers (e.g., types of questions, marks distribution).
2. Generate new question papers based on the identified pattern.

## **Features**
- Upload multiple PDF question papers.
- Analyze patterns of the uploaded papers (e.g., total questions, question types, and marks distribution).
- Generate a new question paper with the same structure.
- Download the newly generated question paper as a `.txt` file.

## **Requirements**
Before running the app, make sure you have the following Python packages installed:
- **Streamlit**: For creating the web interface.
- **PyPDF2**: For extracting text from PDF files.
- **python-dotenv**: For loading API keys securely from a `.env` file.
- **google-generativeai**: For interacting with the Gemini API.

Install the required dependencies by running:
```bash
pip install streamlit pypdf2 python-dotenv google-generativeai
```

## **Setup Instructions**
1. **API Key**:  
   Obtain your **Gemini API key** from Google Cloud and save it in a `.env` file in your project directory:
   ```bash
   API_KEY=your_gemini_api_key
   ```

2. **Run the App**:  
   After installing dependencies and setting up your `.env` file, run the app using:
   ```bash
   streamlit run app.py
   ```

3. **Using the App**:
   - **Upload Question Papers**: Click the "Upload Question Papers" button and select your PDF files.
   - **Analyze Patterns**: Click the "Analyze Patterns" button to analyze the structure of the uploaded papers.
   - **Generate Question Paper**: Click the "Generate Question Paper" button to create a new question paper based on the patterns of the uploaded papers.
   - **Download**: Once the new question paper is generated, you can download it as a `.txt` file.

## **App Workflow**
1. Upload one or more PDF question papers.
2. The app extracts the text and analyzes the structure of the uploaded papers.
3. A new question paper is generated based on the detected pattern, and the user can download it.

## **Note**
- Ensure your **Gemini API key** is valid and properly set up in the `.env` file.
- This app is designed to handle educational question papers, and the output is based on the patterns detected from the uploaded content.
