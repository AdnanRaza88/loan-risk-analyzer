import streamlit as st
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from datetime import datetime

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

if "history" not in st.session_state:
    st.session_state.history = []

# === YEH NAYA CLEAN CSS HAI - AUTO DARK/LIGHT ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }

/* 1. LIGHT MODE DEFAULTS: Sky Blue + White + Firozi */
:root {
    --bg-color: #E0F2FE; /* Sky Blue BG */
    --card-color: #FFFFFF; /* White Card */
    --text-color: #1E293B; /* Dark Text */
    --accent-color: #06B6D4; /* Firozi */
    --subtext-color: #475569;
}
.stApp { background-color: var(--bg-color); }
h1 { color: var(--text-color); }
.glass-card { background: var(--card-color); border-radius: 24px; padding: 2rem; margin: 1.5rem 0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); }
.stButton>button { background: var(--accent-color); color: white; border: none; border-radius: 12px; padding: 0.8rem 1rem; font-weight: 600; width: 100%; }
.stNumberInput input { background: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 12px; color: var(--text-color); }
.field-label { color: var(--subtext-color); }

/* 2. DARK MODE OVERRIDE: Firozi + White + Black */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-color: #0F172A; /* Black BG */
        --card-color: #0E7490; /* Firozi Card */
        --text-color: #F8FAFC; /* White Text */
        --accent-color: #FFFFFF; /* White Button */
        --subtext-color: #CBD5E1;
    }
    .stButton>button { color: var(--bg-color); } /* Black text on white button */
    .stNumberInput input { background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.2); color: white; }
}

/* Result Cards - Both Modes */
.result-card { border-radius: 16px; padding: 1.5rem; margin-top: 2rem; border-left: 5px solid; }
.result-approve { background: #DCFCE7; border-color: #16A34A; }
.result-review { background: #FEF9C3; border-color: #CA8A04; }
.result-reject { background: #FEE2E2; border-color: #DC2626; }
@media (prefers-color-scheme: dark) {
    .result-approve { background: rgba(22, 163, 74, 0.2); }
    .result-review { background: rgba(202, 138, 4, 0.2); }
    .result-reject { background: rgba(220, 38, 38, 0.2); }
}
.history-card { background: var(--card-color); border-radius: 12px; padding: 0.8rem 1rem; margin-bottom: 0.8rem; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>Loan Risk Analyzer</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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

if st.button("Analyze Risk", use_container_width=True):
    applicant_text = f"Annual Income: ${annual_income}, Employment Years: {employment_years}, Credit Score: {credit_score}, Monthly Debts: ${monthly_debts}, Requested Loan: ${loan_amount}, Loan Term: {loan_term} years"
    with st.spinner("Evaluating..."):
        result = structured_llm.invoke(applicant_text)
    
    card_class = "result-approve"
    if result.recommended_action == "Reject": card_class = "result-reject"
    elif result.recommended_action == "Manual Review": card_class = "result-review"

    st.markdown(f"<div class='result-card {card_class}' style='color: var(--text-color);'>", unsafe_allow_html=True)
    st.markdown(f"""<div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem;'>
        <div><span class='field-label'>Risk Level</span><br><strong style='font-size:1.4rem;'>{result.risk_level}</strong></div>
        <div><span class='field-label'>Risk Score</span><br><strong style='font-size:1.4rem;'>{result.risk_score}/100</strong></div>
        <div><span class='field-label'>Action</span><br><strong>{result.recommended_action}</strong></div>
        <div><span class='field-label'>Interest Rate</span><br><strong>{result.suggested_interest_rate:.1f}%</strong></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.history.insert(0, {"time": datetime.now().strftime("%H:%M"), "score": result.risk_score, "action": result.recommended_action, "loan": loan_amount})

if st.session_state.history:
    st.divider()
    st.subheader("Recent Checks")
    for item in st.session_state.history[:5]:
        st.markdown(f"""<div class='history-card' style='color: var(--text-color);'><strong>{item['time']}</strong> | ${item['loan']} | Score: <b>{item['score']}</b> | <b>{item['action']}</b></div>""", unsafe_allow_html=True)
