import streamlit as sl
import sqlite3
from datetime import date

if "username" not in sl.session_state:
    sl.session_state.username = ""


# ---------------- SESSION CHECK (PROTECTION) ----------------------------------
if "logged_in" not in sl.session_state or not sl.session_state.logged_in:
    sl.warning("Please login to access the dashboard.")
    sl.stop()

username=sl.session_state.username

#------------------------PAGE TITLE---------------------------------------------

sl.markdown(
    "<h1 style='text-align:center;color:violet;' >📌 Job Application Tracker</h1>",
    unsafe_allow_html=True
)

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


#==============================DATA SETUP=========================================

DB_NAME="JobQuest.db"

conn=sqlite3.connect(DB_NAME)
cur=conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS job_tracker(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            company TEXT,
            role TEXT,
            location TEXT,
            applied_date TEXT,
            status TEXT,
            source TEXT,
            notes TEXT
            )
""")

conn.commit()
conn.close()

#===========================USER INPUTS==========================================
with sl.form("job_form",clear_on_submit=True):
    company_name=sl.text_input("Company Name")
    role=sl.text_input("Job Role")
    location=sl.text_input("Job Location")
    applied_date=sl.date_input("Date Applied",date.today())
    status=sl.selectbox("Application Status",["Applied", "Under Review", "Interview Scheduled", "Rejected", "Offer Received"])
    source=sl.selectbox("Application Source",["Linkedin","NAukri","Company Website","Referral","Other"])
    notes=sl.text_area("Notes/Remarks")
    col1,col2,col3=sl.columns([2.5,2,1])
    with col1:
        submit=sl.form_submit_button("Save Application",)
    with col2:
        submit_jobs=sl.form_submit_button("My Jobs")
        if submit_jobs:
            sl.switch_page("pages/4_My_Appiled_Jobs.py")
    with col3:
        Back=sl.form_submit_button("Back")
        if Back:
            sl.switch_page("pages/1_Dashboard.py")



if submit:
    if company_name =="" or role == "":
        sl.warning("Company name and Job role are required")

    else:
        sl.success("Application successfully saved")
        conn=sqlite3.connect(DB_NAME)
        cur=conn.cursor()
        cur.execute("""
            INSERT INTO job_tracker
                (username,company,role,location,applied_date,status,source,notes)
                    VALUES (?,?,?,?,?,?,?,?)
        """,(username,company_name,role,location,str(applied_date),status,source,notes))
        
        conn.commit()
        conn.close()
        
