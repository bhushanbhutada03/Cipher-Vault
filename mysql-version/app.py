import streamlit as st
import pandas as pd
from db import insert_password, fetch_all_passwords, fetch_by_website
from main import pass_to_cipher, cipher_to_pass

st.title("Cipher Vault")


# ---------------- ADD PASSWORD ----------------

st.header("Add New Password")

website = st.text_input("Website")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Add Password", key="add"):
    if website and username and password:
        enc_pass = pass_to_cipher(password)
        insert_password(website, username, enc_pass)
        st.success("Password added successfully")
        st.rerun()
    else:
        st.error("All fields required")


# ---------------- VIEW PASSWORDS ----------------

st.header("Stored Credentials")

rows = fetch_all_passwords()

if rows:
    data = []
    for row in rows:
        data.append({"Website": f"https://{row[1]}", "Username": row[2]})

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data found")


# ---------------- SEARCH ----------------

st.header("Search by Website")

search = st.text_input("Enter website")

if st.button("Search", key="search"):
    if search:
        results = fetch_by_website(search)

        if results:
            data = []
            for r in results:
                data.append({"Website": f"https://{r[1]}", "Username": r[2]})

            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No results found")
    else:
        st.error("Enter a website")


# ---------------- ACCESS PASSWORD ----------------

st.header("Access Password")

if rows:
    options = {f"{row[1]} ({row[2]})": row for row in rows}
    selected = st.selectbox("Select entry", list(options.keys()))

    pin_input = st.text_input("Enter PIN", type="password")

    if st.button("Show Password", key="show"):
        if not pin_input.isdigit():
            st.error("Invalid PIN format")
        else:
            p = int(pin_input)

            selected_row = options[selected]
            decrypted = cipher_to_pass(selected_row[3], p)

            if decrypted:
                st.code(decrypted)
            else:
                st.error("Incorrect PIN")
else:
    st.info("No data available")
