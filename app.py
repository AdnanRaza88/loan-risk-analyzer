import streamlit as st
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

class LoanRiskOutput(BaseModel):
    risk_level: str = Field(..., description="Risk level: Low, Medium, High")
    risk_score: int = Field(..., description="Numeric risk score 0-100")
    recommended_action: str = Field(..., description="Action: Approve, Manual Review, Reject")
    suggested_interest_rate: float = Field(..., description="Interest rate to assign based on risk")
    income_stability: str = Field(..., description="Income stability: Low, Medium, High")
    creditworthiness: str = Field(..., description="Overall creditworthiness: Poor, Moderate, Strong")

api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Groq API key not found. Please set it in secrets or .env")
    st.stop()

llm = ChatGroq(api_key=api_key, model="llama-3.1-8b-instant", temperature=0)
structured_llm = llm.with_structured_output(LoanRiskOutput)

st.set_page_config(page_title="Loan Risk Analyzer", layout="centered")

st.markdown("""
<style>
body { background: #f0f2f5; }
.main { max-width: 720px; margin: auto; padding: 2rem; }
.neumorphic {
    background: #ffffff;
    border-radius: 40px;
    box-shadow:  20px 20px 60px #d0d4db, -20px -20px 60px #ffffff;
    padding: 2rem;
    margin: 1.5rem 0;
    transition: 0.2s;
}
.neumorphic:hover {
    box-shadow:  10px 10px 30px #d0d4db, -10px -10px 30px #ffffff;
}
.input-neu {
    background: #f0f2f5;
    border: none;
    border-radius: 30px;
    box-shadow: inset 8px 8px 16px #d0d4db, inset -8px -8px 16px #ffffff;
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
    width: 100%;
    color: #2d3436;
}
.input-neu:focus {
    outline: none;
    box-shadow: inset 4px 4px 8px #d0d4db, inset -4px -4px 8px #ffffff;
}
.btn-neu {
    background: #ffffff;
    border: none;
    border-radius: 50px;
    box-shadow: 8px 8px 16px #d0d4db, -8px -8px 16px #ffffff;
    padding: 0.8rem 2.5rem;
    font-weight: 600;
    color: #2d3436;
    cursor: pointer;
    transition: 0.15s;
    width: 100%;
}
.btn-neu:active {
    box-shadow: inset 8px 8px 16px #d0d4db, inset -8px -8px 16px #ffffff;
}
.result-card {
    background: #ffffff;
    border-radius: 40px;
    box-shadow: inset 6px 6px 12px #d0d4db, inset -6px -6px 12px #ffffff;
    padding: 1.5rem 2rem;
    margin-top: 2rem;
}
.field-label {
    font-weight: 500;
    color: #2d3436;
    margin-bottom: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#2d3436;'>Loan Application Risk Analyzer</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='neumorphic'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        annual_income = st.number_input("Annual Income ($)", min_value=0, step=1000, value=85000)
        employment_years = st.number_input("Years at Current Job", min_value=0.0, step=0.5, value=4.5)
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, step=10, value=720)
    with col2:
        monthly_debts = st.number_input("Monthly Debts ($)", min_value=0, step=100, value=1200)
        loan_amount = st.number_input("Requested Loan Amount ($)", min_value=0, step=1000, value=30000)
        loan_term = st.number_input("Loan Term (Years)", min_value=1, step=1, value=5)
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("Analyze Risk", key="analyze", use_container_width=True):
    applicant_text = f"""
    Annual Income: ${annual_income}
    Employment Years: {employment_years}
    Credit Score: {credit_score}
    Monthly Debts: ${monthly_debts}
    Requested Loan: ${loan_amount}
    Loan Term: {loan_term} years
    """
    with st.spinner("Evaluating application..."):
        result = structured_llm.invoke(applicant_text)
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem;'>
        <div><span class='field-label'>Risk Level</span><br><strong style='font-size:1.4rem;'>{result.risk_level}</strong></div>
        <div><span class='field-label'>Risk Score</span><br><strong style='font-size:1.4rem;'>{result.risk_score}</strong></div>
        <div><span class='field-label'>Recommended Action</span><br><strong>{result.recommended_action}</strong></div>
        <div><span class='field-label'>Interest Rate</span><br><strong>{result.suggested_interest_rate:.1f}%</strong></div>
        <div><span class='field-label'>Income Stability</span><br><strong>{result.income_stability}</strong></div>
        <div><span class='field-label'>Creditworthiness</span><br><strong>{result.creditworthiness}</strong></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)