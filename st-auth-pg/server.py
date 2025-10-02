import streamlit as st
import psycopg2
import bcrypt
import os

def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres.ivuidcuoxxedezilkoze",
        password=os.environ["SUPABASE_DB_PW"],
        host="aws-1-ap-southeast-1.pooler.supabase.com",
        port="5432"
    )

def fetch_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_name, password FROM users WHERE user_name = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def check_password(username, password):
    user = fetch_user(username)

    if user:
        # user[1] is the hashed password in the DB
        return bcrypt.checkpw(password.encode(), user[1].encode())
    return False

# Streamlit login form
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if check_password(username, password):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Invalid credentials.")
else:
    st.write("Welcome! This is your protected content.")
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
