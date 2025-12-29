import streamlit as sl
import sqlite3
import hashlib
import random
import time
from datetime import datetime

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

#======================================CAPTCHA SESSION==================================

if "captcha"  not in sl.session_state:
    sl.session_state.captcha=None

if "captcha_verified" not in sl.session_state:
    sl.session_state.captcha_verified=False

if "captcha_time" not in sl.session_state:
    sl.session_state.captcha_time=None


#===================================HIDE THE ARROW AND THREE DOTS=======================

sl.markdown("""
<style>
    .st-emotion-cache-ujm5ma.ejhh0er0
            {
                visibility:hidden
            }
    .st-emotion-cache-1pbsqtx.ex0cdmw0
            {
                visibility:hidden
            }        
    .st-emotion-cache-1vl639y.e1q4kxr414
            {
                visibility:hidden
            }
""",unsafe_allow_html=True)

#=============================HASH PASSWORD=========================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


DB_NAME= "Jobquest.db"

sl.markdown(
    "<h2 style='text-align:center;'>🔁 Forgot Password – <span style='color:violet;'>JobQuest</span></h2>",
    unsafe_allow_html=True
)


username=sl.text_input("Enter your Username")

#----------------------------CAPTCHA-------------------------------------------------

CAPTCHA_EXPIRY=60
current_time=time.time()

if(
    sl.session_state.captcha is None or
    sl.session_state.captcha_verified is None or
    current_time- sl.session_state.captcha_time > CAPTCHA_EXPIRY):
        sl.session_state.captcha=random.randint(10000,99999)
        sl.session_state.captcha_time=current_time
        sl.session_state.captcha_verified=False



colA,colB=sl.columns(2)
with colA:
    sl.info(f"Captcha Code:{sl.session_state.captcha}")
    remaining=CAPTCHA_EXPIRY - int(current_time - sl.session_state.captcha_time)


with colB:
        if remaining > 0:
            sl.info(f"Captcha expires in {remaining} seconds")
        else:
            sl.warning("Captcha expired. New captcha generated.")


col1,col2=sl.columns([4,1])
    
with col1:
    user_captcha = sl.text_input("Enter Captcha Code",label_visibility="collapsed")
with col2:
    if sl.button("Verify Captcha",disabled=sl.session_state.captcha_verified):
        if user_captcha == str(sl.session_state.captcha):
            sl.session_state.captcha_verified = True
            sl.success("verified ✅")
        
        else:
            sl.error("Wrong ❌")

new_pwd=sl.text_input("New Password",type="password")
conform_pwd=sl.text_input("Conform Password",type="password")

if sl.button("📨 Request Password Reset"):

    if username == "" or new_pwd =="" or conform_pwd =="":
        sl.warning("Please fill all the fields")
    elif new_pwd != conform_pwd:
        sl.warning("Password do not match")
    elif user_captcha != str(sl.session_state.captcha):
        sl.error("Wrong Captcha")
    else:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM APP WHERE username=?",(username,))
        user=cur.fetchone()

        if not user:
            sl.error("Username not found")
        else:
            cur.execute("""
                INSERT INTO password_reset_requests
                (username, new_password, requested_at)
                VALUES (?, ?, ?)
            """, (username, hash_password(new_pwd), datetime.now().strftime("%Y-%m-%d %H:%M")))

            conn.commit()
            conn.close()
            sl.success("Request sent to Admin for approval ✅")
            time.sleep(2)
            sl.switch_page("JobQuest_Login_Page.py")
            
if  remaining>0 and not sl.session_state.captcha_verified:
    time.sleep(1)
    sl.rerun()


