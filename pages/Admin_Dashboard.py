import streamlit as sl
import sqlite3,hashlib
import pandas as pd

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

#=========================PROTECTION===========================================

if "logged_in" not in sl.session_state or not sl.session_state.logged_in:
    sl.stop()

if "role" not in sl.session_state:
    sl.session_state.role=""

if sl.session_state.role != "admin":
    sl.error("Admin only")
    sl.stop()

sl.title("🧑‍💼 Admin Dashboard")
conn=sqlite3.connect("JobQuest.db")



#==================================TOTAL USERS==================================

users=pd.read_sql("SELECT COUNT(*) AS total FROM APP",conn)
sl.metric("👥 Total Users", users.iloc[0]["total"])

sl.divider()


conn = sqlite3.connect("JobQuest.db")
cur = conn.cursor()

#=========================== PASSWORD RESET REQUESTS=========================
cur.execute("""
CREATE TABLE IF NOT EXISTS password_reset_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    new_password TEXT,
    requested_at TEXT,
    status TEXT DEFAULT 'pending'
)
""")
conn.commit()
conn.close()

# 🔐 PASSWORD RESET REQUESTS
sl.subheader("🔐 Password Reset Requests")
conn=sqlite3.connect("JobQuest.db")
requests = pd.read_sql("""
SELECT id, username, requested_at
FROM password_reset_requests
WHERE status='pending'
""", conn)

if requests.empty:
    sl.info("No pending password reset requests")
else:
    sl.dataframe(requests, use_container_width=True)

    req_id = sl.selectbox("Select Request ID", requests["id"])

    col1, col2 = sl.columns(2)

    with col1:
        if sl.button("✅ Approve"):
            cur = conn.cursor()

            # Get password
            cur.execute("""
                SELECT username, new_password
                FROM password_reset_requests
                WHERE id=?
            """, (req_id,))
            data = cur.fetchone()

            # Update user password
            cur.execute("""
                UPDATE APP SET password=?
                WHERE username=?
            """, (data[1], data[0]))

            # Mark request approved
            cur.execute("""
                UPDATE password_reset_requests
                SET status='approved'
                WHERE id=?
            """, (req_id,))

            conn.commit()
            sl.success("Password reset approved")
            sl.rerun()

    with col2:
        if sl.button("❌ Reject"):
            conn.execute("""
                UPDATE password_reset_requests
                SET status='rejected'
                WHERE id=?
            """, (req_id,))
            conn.commit()
            sl.warning("Request rejected")
            sl.rerun()

conn.close()
sl.divider()
if sl.button("🚪 Logout"):
    sl.session_state.clear()
    sl.switch_page("JobQuest_Login_Page.py")

