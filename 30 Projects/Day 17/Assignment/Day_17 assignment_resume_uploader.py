import subprocess
import sys

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "PyPDF2", "pandas"])


import streamlit as st
import PyPDF2
import pandas as pd
import re

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def score_resume(text):
    text = text.lower()
    score = 0

    if len(text.split()) > 400:
        score += 10
    if "skills" in text:
        score += 10
    if "education" in text:
        score += 10
    if "experience" in text or "work history" in text:
        score += 10
    if "project" in text or "achievement" in text:
        score += 10
    if re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text):
        score += 5
    if re.search(r'\b\d{10}\b', text):
        score += 5
    if any(word in text for word in ["developed", "led", "managed", "created", "designed"]):
        score += 10

    return score

st.title("📄 Resume Uploader + Rating App")

uploaded_file = st.file_uploader("Upload a Resume (PDF only)", type=["pdf"])
if uploaded_file is not None:
    st.success("Resume uploaded successfully!")
    
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Preview of Resume Text:")
    st.text(resume_text[:500])  # show only first 500 chars

    score = score_resume(resume_text)
    st.subheader(f"Resume Score: {score}/70")

    df = pd.DataFrame([[uploaded_file.name, score]], columns=["Resume", "Score"])
    df.to_csv("resume_scores.csv", mode='a', header=not pd.io.common.file_exists("resume_scores.csv"), index=False)

