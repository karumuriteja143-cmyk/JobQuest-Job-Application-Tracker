import streamlit as sl
import pypdf
import re
import sqlite3
from datetime import datetime



DB_NAME="JobQuest.db"

if "username" not in sl.session_state:
    sl.session_state.username=""

if "ats_score" not in sl.session_state:
    sl.session_state.ats_score = None

username=sl.session_state.username



#=======================================CSS THEME================================================================
sl.markdown("""
<style>
/* --------- GLOBAL --------- */
html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
    background-color: #0e1117;
}

/* --------- HIDE STREAMLIT UI --------- */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
section[data-testid="stSidebar"] {display: none;}
button[data-testid="collapsedControl"] {display: none;}

/* --------- INPUT FIELDS --------- */
input {
    border-radius: 8px !important;
    padding: 10px !important;
    font-size: 15px !important;
}

/* --------- BUTTONS --------- */
.stButton > button {
    background: linear-gradient(90deg, #8e2de2, #4a00e0);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    opacity: 0.9;
    transform: scale(1.02);
}

/* --------- INFO / WARNING --------- */
.stAlert {
    border-radius: 10px;
}

/* --------- CENTER CONTENT --------- */
.block-container {
    padding-top: 2rem;
    max-width: 700px;
}
</style>
""", unsafe_allow_html=True)

#====================================HIDE SIDEBAR AND ARROW===============================================================

sl.markdown("""
<style>
/* Hide sidebar */
section[data-testid="stSidebar"] {
    display: none;
}

/* Hide sidebar toggle arrow */
button[data-testid="collapsedControl"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)


sl.markdown("""
<style>
            .st-emotion-cache-pkm19r.e1q4kxr415
            {
                visibility:hidden;
            }
            .st-emotion-cache-1wbqy5l.e17qgqm80
            {
                visibility:hidden;
            }
</style>
""",unsafe_allow_html=True)

#-------------------------------DATABASE------------------------------------------
#=============================CREATE TABLE=======================================

def create_ats_table():
    conn=sqlite3.connect(DB_NAME)
    cur=conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ATS_REPORTS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            resume_name TEXT,
            ats_source INTEGER,
            analysis_date TEXT
            )
""")
    conn.commit()
    conn.close()

#=============================SAVE ATS RESULT====================================

def save_ats_result(username,ats_source):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO ATS_REPORTS (username, ats_source, analysis_date)
        VALUES (?, ?, ?)
    """, (
        username,
        ats_source,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ================= TOTAL RESUME COUNT =================
def get_total_resumes(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM ATS_REPORTS WHERE username=?",
        (username,)
    )
    count = cur.fetchone()[0]

    conn.close()
    return count


# ================= RECENT ACTIVITY =================
def get_recent_activity(username, limit=5):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT ats_score, analysis_date
        FROM ATS_REPORTS
        WHERE username=?
        ORDER BY id DESC
        LIMIT ?
    """, (username, limit))

    data = cur.fetchall()
    conn.close()
    return data
# ------------------------- SESSION PROTECTION ---------------------------------
if "logged_in" not in sl.session_state or not sl.session_state.logged_in:
    sl.warning("Please login to access this page.")
    sl.stop()

#=========================PAGE PROTECTION=======================================

sl.markdown(
    "<h1 style='text-align:center;color:violet;'>📄ATS Resume Analyzer </h1> ",
    unsafe_allow_html=True
)

sl.write("Upload your resume and paste the job description to check ATS compatibility")

#==============================SKILL KEYWORDS===================================

SKILLS = [
    "python", "sql", "java", "c++", "dsa", "data structures",
    "algorithms", "django", "flask", "streamlit",
    "html", "css", "javascript", "react",
    "git", "github", "linux",
    "aws", "azure", "docker", "api"
]

#=============================FUNCTIONS=========================================

def extract_text_from_pdf(pdf_file):
    reader=pypdf.PdfReader(pdf_file)
    text=""
    for page in reader.pages:
        text+=page.extract_text()
    return text.lower()

def extract_skills(text):
    found_skills = set()
    for skill in SKILLS:
        if re.search(rf"\b{skill}\b", text):
            found_skills.add(skill)
    return found_skills

# ----------------- UI INPUTS -----------------
resume_file = sl.file_uploader("📤 Upload Resume (PDF only)", type=["pdf"])
job_desc = sl.text_area("📋 Paste Job Description here")

#=============================ANALYSIS==========================================
col1,col2,col3=sl.columns([6,1,1])
with col1:
    if sl.button("Analyze Resume"):
        if resume_file is None or job_desc.strip()=="":
            sl.warning("Please upload resume and paste job description.")
            sl.stop()

        resume_text = extract_text_from_pdf(resume_file)
        job_text = job_desc.lower()

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_text)

        matched_skills = resume_skills.intersection(job_skills)
        missing_skills = job_skills - resume_skills

        if len(job_skills) == 0:
            sl.error("No recognizable skills found in job description.")
            sl.stop()

        source = int((len(matched_skills) / len(job_skills)) * 100)
        sl.session_state.ats_score = source
        sl.session_state.matched_skills = matched_skills
        sl.session_state.missing_skills = missing_skills

        save_ats_result(username,source)

with col2:
    pass

with col3:
    if sl.button("Back"):
        sl.switch_page("pages/1_Dashboard.py")
        sl.rerun()

    
# ----------------- RESULTS -----------------
if sl.session_state.ats_score is not None:
    source = sl.session_state.ats_score
    matched_skills = sl.session_state.matched_skills
    missing_skills = sl.session_state.missing_skills
    sl.subheader("📊 ATS Match Score")
    sl.progress(source)
    sl.success(f"Your ATS Score: {source}%")

    col1, col2 = sl.columns(2)

    with col1:
        sl.subheader("✅ Matched Skills")
        if matched_skills:
            for skill in sorted(matched_skills):
                sl.write(f"✔ {skill}")
        else:
            sl.write("No matched skills")

    with col2:
        sl.subheader("❌ Missing Skills")
    if missing_skills:
        for skill in sorted(missing_skills):
            sl.write(f"✘ {skill}")
    else:
        sl.write("No missing skills 🎉")

# ----------------- SUGGESTION -----------------
    sl.subheader("📝 ATS Improvement Tip")
    if source < 50:
        sl.warning("Add missing skills to your resume to improve ATS score.")
    elif source < 80:
        sl.info("Good match! Minor improvements recommended.")
    else:
        sl.success("Excellent ATS compatibility!")


