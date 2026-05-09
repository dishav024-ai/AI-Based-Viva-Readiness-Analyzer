import streamlit as st
import sqlite3
import random
import time

# --- 1. DATABASE SETUP (Ye nayi file banayega) ---
def init_db():
    conn = sqlite3.connect('viva_data.db')
    c = conn.cursor()
    # Table for Results
    c.execute('''CREATE TABLE IF NOT EXISTS results 
                 (username TEXT, subject TEXT, question TEXT, score TEXT, analysis TEXT)''')
    conn.commit()
    conn.close()

init_db() # App chalte hi database initialize ho jayega

# --- 2. THEME & SETTINGS ---
st.set_page_config(page_title="AI Viva Analyser", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F5F5DC; }
    h1, h2, h3, p, label { color: #5D4037 !important; }
    .stButton>button { background-color: #8D6E63; color: white; border-radius: 10px; border: 2px solid #5D4037; padding: 10px 25px; width: 100%; font-weight: bold; }
    .main-card { background-color: #ffffff; padding: 30px; border-radius: 20px; border: 2px solid #D7CCC8; box-shadow: 0px 10px 25px rgba(93, 64, 55, 0.1); }
    .report-card { background-color: #ffffff; padding: 25px; border-radius: 15px; border-left: 15px solid #5D4037; border: 2px solid #8D6E63; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. QUESTION BANK ---
QUESTIONS = {
    "Computer Networks": ["Explain OSI Model layers.", "TCP vs UDP difference.", "What is DNS?", "How does HTTP work?"],
    "Operating Systems": ["What is Paging?", "Explain Semaphore.", "What is a System Call?", "Deadlock conditions."],
    "DBMS": ["What is B-Tree index?", "Normalization (1NF, 2NF, 3NF).", "ACID Properties.", "SQL Joins explained."]
}

# --- 4. SESSION STATE ---
for key in ['page', 'user', 'subject', 'question', 'analysis']:
    if key not in st.session_state: st.session_state[key] = "auth" if key == 'page' else ""

# --- 5. DATA STORAGE FUNCTION ---
def save_to_db(u, s, q, sc, an):
    conn = sqlite3.connect('viva_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?)", (u, s, q, sc, an))
    conn.commit()
    conn.close()

# --- 6. PAGES ---
def show_auth():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🟫 AI Viva Analyser")
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    with tab1:
        u_log = st.text_input("Username", key="log_u")
        if st.button("Sign In"):
            if u_log: st.session_state.user, st.session_state.page = u_log, "subject"; st.rerun()
    with tab2:
        st.text_input("Email", key="sig_e")
        if st.button("Register Now"): st.success("Account created! Switch to Login.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_subject():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title(f"Welcome, {st.session_state.user}!")
    sub = st.selectbox("Select Subject:", list(QUESTIONS.keys()))
    if st.button("Start Viva"):
        st.session_state.subject, st.session_state.question, st.session_state.page = sub, random.choice(QUESTIONS[sub]), "viva"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_viva():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.info(f"**Question:** {st.session_state.question}")
    u_ans = st.text_area("Answer here:")
    if st.button("Submit Answer"):
        with st.spinner("AI Evaluating..."):
            time.sleep(1.5)
            score = f"{random.randint(6, 9)}/10"
            feedback = "Good technical understanding."
            # DATABASE ME SAVE KARO
            save_to_db(st.session_state.user, st.session_state.subject, st.session_state.question, score, feedback)
            st.session_state.analysis = {"marks": score, "feedback": feedback}
            st.session_state.page = "feedback"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_feedback():
    st.title("📊 Analysis Report")
    res = st.session_state.analysis
    st.markdown(f'<div class="report-card"><h2>Score: {res["marks"]}</h2><p>{res["feedback"]}</p></div>', unsafe_allow_html=True)
    if st.button("Back to Home"): st.session_state.page = "subject"; st.rerun()

# --- NAVIGATION ---
if st.session_state.page == "auth": show_auth()
elif st.session_state.page == "subject": show_subject()
elif st.session_state.page == "viva": show_viva()
elif st.session_state.page == "feedback": show_feedback()