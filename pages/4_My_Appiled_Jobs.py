import streamlit as sl
import sqlite3
import pandas as pd

if "username" not in sl.session_state:
    sl.session_state.username=""


# ---------------- SESSION CHECK (PROTECTION) ----------------------------------
if "logged_in" not in sl.session_state or not sl.session_state.logged_in:
    sl.warning("Please login to access the dashboard.")
    sl.stop()



#=============================PAGE TITLE=========================================

sl.markdown(
    "<h1 style 'text.align:center;color:violet;'>📄 My Applied Jobs</h1>",unsafe_allow_html=True)

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

#===============================MY APPLIED JOBS=====================================


DB_NAME = "JobQuest.db"
username = sl.session_state.username

conn = sqlite3.connect(DB_NAME)

query = """
SELECT
    id,
    company AS "Company",
    role AS "Job Role",
    location AS "Location",
    applied_date AS "Applied Date",
    status AS "Status",
    source AS "Source",
    notes AS "Notes"
FROM job_tracker
WHERE username = ?
"""

df = pd.read_sql_query(query, conn, params=(username,))
conn.close()


# -------- SHOW TABLE ----------
if df.empty:
    sl.info("No jobs found")
else:
    sl.dataframe(
                df,
                use_container_width=True,
                hide_index=True)

    # -------- DELETE SECTION ----------
    sl.subheader("🗑 Delete a Job")

job_id = sl.selectbox(
    "Select Job ID to delete",
    df["id"]
)
col1,col2,col3=sl.columns([3,4.7,3])
with col1:
    if sl.button("Delete Selected Job"):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM job_tracker WHERE id=? AND username=?",
            (job_id, username)
        )
        conn.commit()
        conn.close()

        sl.success("Job deleted successfully")
        sl.rerun()
with col2:
    pass

with col3:
    # -------- BACK BUTTON ----------
    if sl.button("⬅ Back to Job Tracker"):
        sl.switch_page("pages/3_Jobs_Applies.py")

