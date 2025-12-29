import streamlit as sl
import sqlite3
import hashlib
import random
import time
import re

#============================================PASSWORD STRENGTH METER==========================================


def password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[@$!%*?&]", password):
        score += 1

    return score




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



#================================================HASH PASSWORD============================================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


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

sl.markdown("<h1 style=text-align:center;color:violet>WELCOME TO JOBQUEST APP</h1>",unsafe_allow_html=True)
#=============================CAPTCHA SESSION========================================================================
if "captcha" not in sl.session_state:
    sl.session_state.captcha = None

if "captcha_verified" not in sl.session_state:
    sl.session_state.captcha_verified = False

if "captcha_time" not in sl.session_state:
    sl.session_state.captcha_time = None


if "current_page" not in sl.session_state:
    sl.session_state.current_page = "Login"

if "role" not in sl.session_state:
    sl.session_state.role=""



#--------------------------------DATABASE--------------------------------------------------------------------

DB_NAME = "Jobquest.db"
conn=sqlite3.connect(DB_NAME)
cur=conn.cursor()


cur.execute("""
        CREATE TABLE IF NOT EXISTS APP (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email_address TEXT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT default 'user'
            )

""")
conn.commit()
conn.close()

choice = sl.selectbox(
    "Login/Sign Up",
    ["Login", "Sign Up"],
    index=0 if sl.session_state.current_page == "Login" else 1
)

sl.session_state.current_page = choice


#----------------------------------LOGIN--------------------------------------------------------------------------


if sl.session_state.current_page == "Login":
    User_name=sl.text_input("Enter the Username")
    login_password=sl.text_input("Password",type="password")
    # 🔁 LINK TO FORGOT PASSWORD (NEW TAB)
    sl.markdown(
    '<a href="/Forgot_Password" target="_blank"> Forgot Password?</a>',
    unsafe_allow_html=True
    )
    if sl.button("Submit"):
        if User_name=="" or login_password=="":
            sl.warning("Please enter both fields")
        else:
            conn = sqlite3.connect(DB_NAME)
            cur=conn.cursor()
            hashed_pwd = hash_password(login_password)
            cur.execute("""
                SELECT * FROM APP
                        WHERE username=? AND password=?
            """,(User_name,hashed_pwd))
            user= cur.fetchone()
            conn.close()

            if user:
                sl.session_state.logged_in = True
                sl.session_state.username = user[3]
                sl.session_state.role=user[5]

                if sl.session_state.role  == "admin":
                    sl.switch_page("pages/Admin_Dashboard.py")
                else:
                    sl.switch_page("pages/1_Dashboard.py")

            else:
                sl.error("Invalid Username or Password")
            

    

#------------------------------------SIGN UP-----------------------------------------------------------------------

else:
    name=sl.text_input("Enter your Fullname")
    email=sl.text_input("Enter your Email Address",placeholder="example@gmail.com")
    user_name=sl.text_input("Create Unique USername")
    signup_password=sl.text_input("Create Password",type="password",key="signup_password")

    strength = password_strength(signup_password)

    if signup_password:
        if strength <= 2:
            sl.error("🔴 Weak password")
            
        elif strength == 3:
            sl.warning("🟡 Medium password")
            
        else:
            sl.success("🟢 Strong password")

    con_password=sl.text_input("Conform Password",type="password",key="signup_confirm_password")
    # ---------- CAPTCHA -----------------------------------------------
    CAPTCHA_EXPIRY=30
    current_time=time.time()

    if (
    sl.session_state.captcha is None or
    sl.session_state.captcha_time is None or
    current_time - sl.session_state.captcha_time > CAPTCHA_EXPIRY):
        sl.session_state.captcha = random.randint(100000, 999999)
        sl.session_state.captcha_time = current_time
        sl.session_state.captcha_verified = False
    
    colA,colB=sl.columns(2)
    with colA:
        sl.info(f"Captcha Code: {sl.session_state.captcha}")
        remaining = CAPTCHA_EXPIRY - int(current_time - sl.session_state.captcha_time)
        
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

    if sl.button("Create your Account"):
        if password_strength(signup_password) < 3:
            sl.warning("Please choose a stronger password")
            sl.stop()

        if not sl.session_state.captcha_verified:
            sl.warning("Please verify captcha first")
            sl.rerun()
        if user_name=="" or name=="" or email=="" or signup_password=="" or con_password=="":
            sl.warning("Please enter all fields")
        elif len(signup_password) < 8:
            sl.warning("Password must be at least 8 character")
        elif signup_password != con_password:
            sl.warning("Passwords not matched")
        else:
            conn = sqlite3.connect(DB_NAME)
            cur=conn.cursor()

            # check duplicate username
            cur.execute("SELECT * FROM APP WHERE username=?",(user_name,))
            existing = cur.fetchone()

            if existing:
                sl.warning("Username already exists. Choose another one.")
            else:
                hashed_pwd = hash_password(signup_password)


                cur.execute("""INSERT INTO APP
                    (full_name,email_address,username,password)
                    VALUES (?,?,?,?)
                """,(name,email,user_name,hashed_pwd))
                conn.commit()
                conn.close()

                sl.success("Account Created Successfully ✅ Redirecting to login...")
                time.sleep(1)
                sl.session_state.current_page = "Login"
                sl.rerun()

    if  remaining > 0 and not sl.session_state.captcha_verified:
        time.sleep(1)
        sl.rerun()




        