import streamlit as stm
from pypdf import PdfReader

stm.set_page_config(page_title="AI Resume Matcher", layout="wide")

stm.title("🎯 Smart Resume & Job Matcher")
stm.write("Match your resume against any job description to check alignment.")

col1, col2 = stm.columns(2)

with col1:
    job_desc = stm.text_area("1. Paste Job Description (JD):", height=250)

with col2:
    uploaded_file = stm.file_uploader("2. Upload Resume (PDF)", type=["pdf"])
    resume_text_manual = stm.text_area("Or Paste Resume Text here:", height=150)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text

# Function to extract clean words
def extract_keywords(text):
    clean_text = text.lower().replace(",", " ").replace(".", " ").replace(":", " ")
    return set(clean_text.split())

if stm.button("Analyze Match"):
    resume_text = ""
    
    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
    elif resume_text_manual.strip():
        resume_text = resume_text_manual.strip()

    if job_desc and resume_text:
        jd_words = extract_keywords(job_desc)
        resume_words = extract_keywords(resume_text)

        stopwords = {
            "and", "the", "to", "in", "for", "a", "of", "with", "is", "on", 
            "an", "at", "as", "by", "from", "that", "this", "be", "are", "or"
        }
        jd_keywords = jd_words - stopwords

        if jd_keywords:
            matched_words = jd_keywords.intersection(resume_words)
            score = round((len(matched_words) / len(jd_keywords)) * 100, 2)

            stm.divider()
            stm.metric("Match Score", f"{score}%")
            
            res_col1, res_col2 = stm.columns(2)
            with res_col1:
                stm.subheader("✅ Matched Keywords")
                stm.write(", ".join(matched_words) if matched_words else "No keywords matched.")

            with res_col2:
                missing_words = jd_keywords - resume_words
                stm.subheader("⚠️ Missing Keywords (To Add)")
                stm.write(", ".join(list(missing_words)[:20]))
        else:
            stm.warning("Please provide more details in the Job Description.")
    else:
        stm.warning("Please provide both Job Description and Resume (upload PDF or paste text).")