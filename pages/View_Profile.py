import streamlit as sl
import sqlite3

# ---------------- SESSION PROTECTION ----------------
if "logged_in" not in sl.session_state or not sl.session_state.logged_in:
    sl.warning("Please login first")
    sl.stop()

username = sl.session_state.username
role = sl.session_state.role

# ---------------- PAGE TITLE ----------------
sl.markdown(
    "<h1 style='text-align:center;color:violet;'>👤 View Profile</h1>",
    unsafe_allow_html=True
)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("JobQuest.db")
cur = conn.cursor()

cur.execute("""
SELECT full_name, email_address, username, role
FROM APP
WHERE username = ?
""", (username,))

user = cur.fetchone()
conn.close()

#===============================================CSS THEME======================================================
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


# ---------------- PROFILE CARD ----------------
if user:
    full_name, email, uname, role = user

    sl.markdown(
        f"""
        <div style="
            background:#161b22;
            padding:20px;
            border-radius:12px;
            border:1px solid #30363d;
        ">
            <h3>👤 {full_name}</h3>
            <p><b>Username:</b> {uname}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Role:</b> {role}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    sl.error("Profile not found")

sl.divider()

# ---------------- PLACEHOLDER MESSAGE ----------------
sl.info("🛠 Profile editing feature will be added soon.")

# ---------------- BACK BUTTON ----------------
if sl.button("⬅ Back to Dashboard"):
    sl.switch_page("pages/1_Dashboard.py")
