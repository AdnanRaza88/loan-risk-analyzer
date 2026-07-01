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

# === YEH NAYA GLASSMORPHISM CSS HAI ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="st-"] { font-family: 'Poppins', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); /* Dark Blue Gradient BG */
}
h1 { color: #fff; text-shadow: 0 0 15px rgba(124, 58, 237, 0.5); } /* Glow Title */

/* Glass Card */
.glass-card {
    background: rgba(255, 255, 255, 0.05); /* Transparent */
    backdrop-filter: blur(15px); /* Blur Effect = Glass */
    -webkit-backdrop-filter: blur(15px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

/* Fancy Button */
.stButton>button {
    background: linear-gradient(90deg, #7C3AED, #EC4899); /* Purple to Pink */
    color: white; border: none; border-radius: 12px;
    padding: 0.8rem 1rem; font-weight: 600; width: 100%;
    transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
}
.stButton>button:hover {
    transform: translateY(-2px); box-shadow: 0 6px 20px rgba(236, 72, 153, 0.5);
}

/* Input Box Dark */
.stNumberInput input {
    background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px; color: white;
}

/* Color Result Cards Dark Theme */
.result-card-approve { background: rgba(46, 125, 50, 0.2); border-left: 5px solid #2E7D32; padding: 1.5rem; border-radius: 16px; margin-top: 2rem; }
.result-card-review { background: rgba(249, 168, 37, 0.2); border-left: 5px solid #F9A825; padding: 1.5rem; border-radius: 16px; margin-top: 2rem; }
.result-card-reject { background: rgba(198, 40, 40, 0.2); border-left: 5px solid #C62828; padding: 1.5rem; border-radius: 16px; margin-top: 2rem; }
.field-label { font-weight: 400; color: #a0aec0; font-size: 0.9rem; }
.history-card { background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 0.8rem 1rem; margin-bottom: 0.8rem; border: 1px solid rgba(255, 255, 255, 0.1); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>Loan Risk Analyzer AI</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True) # Glass Card Start
    col1, col2 = st.columns(2)
    with col1:
        annual_income = st.number_input("Annual Income ($)", min_value=0, step=1000, value=85000)
        employment_years = st.number_input("Years at Current Job", min_value=0.0, step=0.5, value=4.5)
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, step=10, value=720)
    with col2:
        monthly_debts = st.number_input("Monthly Debts ($)", min_value=0, step=100, value=1200)
        loan_amount = st.number_input("Requested Loan Amount ($)", min_value=0, step=1000, value=30000)
        loan_term = st.number_input("Loan Term (Years)", min_value=1, step=1, value=5)
    st.markdown("</div>", unsafe_allow_html=True) # Glass Card End

if st.button("Analyze Risk 🔥", use_container_width=True):
    applicant_text = f"Annual Income: ${annual_income}, Employment Years: {employment_years}, Credit Score: {credit_score}, Monthly Debts: ${monthly_debts}, Requested Loan: ${loan_amount}, Loan Term: {loan_term} years"
    with st.spinner("AI Evaluating..."):
        result = structured_llm.invoke(applicant_text)
    
    card_class = "result-card-approve"
    if result.recommended_action == "Reject": card_class = "result-card-reject"
    elif result.recommended_action == "Manual Review": card_class = "result-card-review"

    st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
    st.markdown(f"""<div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem; color:white;'>
        <div><span class='field-label'>Risk Level</span><br><strong style='font-size:1.4rem;'>{result.risk_level}</strong></div>
        <div><span class='field-label'>Risk Score</span><br><strong style='font-size:1.4rem;'>{result.risk_score}/100</strong></div>
        <div><span class='field-label'>Action</span><br><strong>{result.recommended_action}</strong></div>
        <div><span class='field-label'>Interest Rate</span><br><strong>{result.suggested_interest_rate:.1f}%</strong></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.history.insert(0, {"time": datetime.now().strftime("%H:%M"), "score": result.risk_score, "action": result.recommended_action, "loan": loan_amount})

if st.session_state.history:
    st.divider()
    st.subheader("📜 Recent Checks", divider=False)
    for item in st.session_state.history[:5]:
        st.markdown(f"""<div class='history-card'><strong>{item['time']}</strong> | ${item['loan']} | Score: <b>{item['score']}</b> | <b>{item['action']}</b></div>""", unsafe_allow_html=True)
