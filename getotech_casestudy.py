import streamlit as st
import pandas as pd
import os

DATA_FILE = "candidates.csv"

def load_candidates():
    if os.path.exists(DATA_FILE):
        # Read all columns as strings to prevent auto-formatting issues.
        return pd.read_csv(DATA_FILE, dtype={"Name": str, "FatherName": str, "Phone": str})
    else:
        return pd.DataFrame(columns=["Name", "FatherName", "Phone"])

def save_candidates(df):
    df.to_csv(DATA_FILE, index=False)

st.title("Candidate Info Manager")

# Sidebar navigation using radio buttons
operation = st.sidebar.radio("Select Operation", ("Register Candidate", "Search Candidate"))

if operation == "Register Candidate":
    st.header("Candidate Registration")
    candidate_name = st.text_input("Candidate Name")
    father_name = st.text_input("Father's Name")
    phone_number = st.text_input("Phone Number")
    
    if st.button("Submit"):
        if candidate_name and father_name and phone_number:
            # Remove commas and extra whitespace from the phone number
            phone_number = phone_number.replace(",", "").strip()
            # Strict check: Phone number must be exactly 10 digits long and only contain digits.
            if len(phone_number) != 10 or not phone_number.isdigit():
                st.error("Phone number must be exactly 10 digits long and contain only numeric digits (no letters or symbols).")
            else:
                candidates_df = load_candidates()
                # Check for duplicate candidate names (case-insensitive)
                duplicate = candidates_df[candidates_df["Name"].str.lower() == candidate_name.lower()]
                if not duplicate.empty:
                    st.warning("This candidate is already registered.")
                else:
                    new_entry = pd.DataFrame([{
                        "Name": candidate_name, 
                        "FatherName": father_name, 
                        "Phone": phone_number
                    }])
                    candidates_df = pd.concat([candidates_df, new_entry], ignore_index=True)
                    save_candidates(candidates_df)
                    st.success("Candidate registered successfully!")
        else:
            st.error("All fields are required.")

elif operation == "Search Candidate":
    st.header("Candidate Lookup")
    search_term = st.text_input("Enter a part or full candidate name")
    
    if st.button("Search"):
        candidates_df = load_candidates()
        if search_term:
            # Perform a case-insensitive substring search on candidate names
            results = candidates_df[candidates_df["Name"].str.contains(search_term, case=False, na=False)]
            if not results.empty:
                st.write("### Matching Candidates")
                st.dataframe(results)
            else:
                st.warning("No candidate found matching that name.")
        else:
            st.error("Please enter a search term.")
