import streamlit as st
import json

# Upload contract
document = st.file_uploader("Upload Contract", accept_multiple_files=False)
document_name = ".".join(document.name.split(".")[:-1]) if document else "Unnamed_document"

# Text inputs for agreement details
agreement_type = st.text_input("Enter agreement type")
applicable_law = st.text_input("Enter applicable law")
sector = st.text_input("Enter sector")

# Initialize session state for reviews and clauses if they don't exist
if "reviews" not in st.session_state:
    st.session_state.reviews = []

if "clauses" not in st.session_state:
    st.session_state.clauses = {}

# Function to add a new party
def add_new_party():
    st.session_state.reviews.append("")

# Function to delete a party
def delete_party(index):
    st.session_state.reviews.pop(index)
    if index in st.session_state.clauses:
        del st.session_state.clauses[index]
    # Adjust the keys in st.session_state.clauses if necessary
    for i in range(index + 1, len(st.session_state.reviews) + 1):
        if i in st.session_state.clauses:
            st.session_state.clauses[i - 1] = st.session_state.clauses.pop(i)

# Function to add a new clause for a party
def add_new_clause(party_index):
    if party_index not in st.session_state.clauses:
        st.session_state.clauses[party_index] = []
    st.session_state.clauses[party_index].append({"clause_number": "", "clause_text": "", "clause_correction": "", "comment": ""})

# Function to delete a clause for a party
def delete_clause(party_index, clause_index):
    st.session_state.clauses[party_index].pop(clause_index)

# Button to add a new party
if st.button("Add party"):
    add_new_party()

# Display text inputs for each party in the session state
for i, review in enumerate(st.session_state.reviews):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.session_state.reviews[i] = st.text_input(f"Enter party {i + 1} name", value=review, key=f"party_{i}")
    with col2:
        if st.button(f"Delete party {i + 1}", key=f"delete_party_{i}"):
            delete_party(i)
            st.experimental_rerun()

    # Button to add a new clause for this party
    if st.button(f"Add clause for Party {i + 1}", key=f"add_clause_{i}"):
        add_new_clause(i)

    # Display clause inputs for this party
    if i in st.session_state.clauses:
        for j, clause in enumerate(st.session_state.clauses[i]):
            st.session_state.clauses[i][j]["clause_number"] = st.text_input(f"Party {i + 1} Clause {j + 1} Number", value=clause["clause_number"], key=f"party_{i}_clause_{j}_number")
            st.session_state.clauses[i][j]["clause_text"] = st.text_area(f"Party {i + 1} Clause {j + 1} Text", value=clause["clause_text"], key=f"party_{i}_clause_{j}_text")
            st.session_state.clauses[i][j]["clause_correction"] = st.text_area(f"Party {i + 1} Clause {j + 1} Correction", value=clause["clause_correction"], key=f"party_{i}_clause_{j}_correction")
            st.session_state.clauses[i][j]["comment"] = st.text_input(f"Party {i + 1} Clause {j + 1} Comment", value=clause["comment"], key=f"party_{i}_clause_{j}_comment")
            if st.button(f"Delete Clause {j + 1} for Party {i + 1}", key=f"delete_clause_{i}_{j}"):
                delete_clause(i, j)
                st.experimental_rerun()

# Function to create the JSON data
def create_json_file():
    data = {
        "title": document_name,
        "agreement_type": agreement_type,
        "applicable_law": applicable_law,
        "sector": sector,
        "reviews": []
    }

    for i, review in enumerate(st.session_state.reviews):
        party_data = {
            "party": review,
            "corrections": []
        }
        if i in st.session_state.clauses:
            for clause in st.session_state.clauses[i]:
                clause_data = {
                    "clause_no": clause["clause_number"],
                    "clause_text": clause["clause_text"],
                    "clause_correction": clause["clause_correction"],
                    "comment": clause["comment"]
                }
                party_data["corrections"].append(clause_data)
        data["reviews"].append(party_data)

    json_data = json.dumps(data, indent=4)
    return json_data

# Button to download the JSON file
if st.button("Create JSON"):
    json_data = create_json_file()
    st.download_button(
        label="Download JSON file",
        data=json_data,
        file_name=f"{document_name}-label.json",
        mime="application/json"
    )