# Loan Risk Analyzer

A Streamlit web application for analyzing loan application risk using Groq's Llama model via LangChain.

## Features
- Real-time loan risk assessment
- Structured output with Pydantic models
- Modern neumorphic UI design
- Risk level, score, recommended action, suggested interest rate, etc.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AdnanRaza88/loan-risk-analyzer.git
   cd loan-risk-analyzer
   ```
2. Install dependencies:
   ```bash
   pip install streamlit langchain-groq pydantic python-dotenv
   ```
3. Set your Groq API key:
   - Create `.env` file with `GROQ_API_KEY=your_key_here`
   - Or set it in Streamlit Cloud secrets

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deployment
Deploy easily on [Streamlit Cloud](https://streamlit.io/cloud) by connecting this GitHub repo.

## Requirements
- Groq API Key (free tier available)
- Python 3.8+

Made for assignment/demo purposes.