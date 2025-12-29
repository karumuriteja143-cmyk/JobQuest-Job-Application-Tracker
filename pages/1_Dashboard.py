import streamlit as sl
import sqlite3

if "chat_history" not in sl.session_state:
    sl.session_state.chat_history = []

if "chat_input" not in sl.session_state:
    sl.session_state.chat_input = ""


if "username" not in sl.session_state:
    sl.session_state.username = ""

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

# ---------------- SESSION CHECK (PROTECTION) ----------------------------------
if "logged_in" not in sl.session_state or not sl.session_state.logged_in:
    sl.warning("Please login to access the dashboard.")
    sl.stop()


#------------------------PAGE TITLE---------------------------------------------

sl.markdown(
    "<h1 style='text-align:center;color:violet;' >📊 JobQuest Dashboard</h1>",
    unsafe_allow_html=True
)

sl.markdown(
    f"<p style='text-align:center;'>Welcome back, <b>{sl.session_state.username}</b> 👋</p>",
    unsafe_allow_html=True
)
sl.divider()

#==============================FOR DATABASE======================================
DB_NAME = "JobQuest.db"
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# ---------------- ATS METRICS (REAL DATA) ----------------

# Total resumes analyzed
total_resumes = cur.execute(
    "SELECT COUNT(*) FROM ATS_REPORTS WHERE username=?",
    (sl.session_state.username,)
).fetchone()[0]

total_jobs=cur.execute(
    "SELECT COUNT(*) FROM job_tracker WHERE username=?",
    (sl.session_state.username,)
).fetchone()[0]
profile_status = "Complete"



# ---------------- DASHBOARD METRICS ----------------


col1, col2, col3 = sl.columns(3)

with col1:
    sl.metric(label="📄 Resumes Analyzed",value= total_resumes)

with col2:
    sl.metric(label="📌 Jobs Applied", value=total_jobs)

with col3:
    sl.metric(label="👤 Profile Status", value=profile_status)

sl.divider()

recent_activity = cur.execute("""
    SELECT ats_score, analysis_date
    FROM ATS_REPORTS
    WHERE username=?
    ORDER BY id DESC
    LIMIT 5
""", (sl.session_state.username,)).fetchall()


# ---------------- QUICK ACTIONS ----------------
sl.subheader("🚀 Quick Actions")

colA, colB, colC = sl.columns(3)

with colA:
    if sl.button("📄 Analyze Resume"):
        sl.switch_page("pages/2_ATS_Resume_Analyzer.py")


with colB:
    if sl.button("📌 Add Job"):
        sl.switch_page("pages/3_Jobs_Applies.py")

with colC:
    if sl.button("👤 View Profile"):
        sl.switch_page("pages/View_Profile.py")

sl.divider()

# ---------------- RECENT ACTIVITY ----------------
sl.subheader("🕒 Recent Activity")

if recent_activity:
    for score, date in recent_activity:
        sl.write(f"📄 Resume analyzed — **Score:** {score}% | 🕒 {date}")
else:
    sl.info("No recent activity yet.")

conn.close()

# ---------------- LOGOUT ----------------
sl.divider()
if sl.button("🚪 Logout"):
    sl.session_state.logged_in = False
    sl.session_state.username = ""
    sl.success("Logged out successfully")
    sl.switch_page("JobQuest_login_page.py")
    sl.rerun()


# ---------- CHAT STATE ----------

sl.subheader("🤖 JobQuest Assistant")

with sl.form("chat_form", clear_on_submit=True):
    user_msg = sl.text_input("Ask about ATS, resume, jobs, dashboard, profile")
    send = sl.form_submit_button("Send")

if send and user_msg:
    msg = user_msg.lower()

    if "ats" in msg:
        reply = (
            "ATS (Applicant Tracking System) evaluates resumes using keywords, "
            "skills, and job relevance to shortlist candidates."
        )
    elif "resume" in msg:
        reply = "Upload your resume to analyze skills and calculate ATS score."
    elif "job" in msg:
        reply = "You can add jobs and track applications in JobQuest."
    elif "dashboard" in msg:
        reply = "Dashboard shows resumes analyzed, recent activity, and actions."
    elif "profile" in msg:
        reply = "Profile stores your personal and professional details."
    else:
        reply = "Please ask about ATS, resume, jobs, dashboard, or profile."

    sl.session_state.chat_history.append(("You", user_msg))
    sl.session_state.chat_history.append(("Bot", reply))

# ---------- DISPLAY CHAT ----------
for sender, text in sl.session_state.chat_history:
    if sender == "You":
        sl.markdown(f"**🧑 You:** {text}")
    else:
        sl.markdown(f"**🤖 Assistant:** {text}")



