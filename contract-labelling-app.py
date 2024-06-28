import streamlit as st
import json

# Upload contract
document = st.file_uploader("Upload Contract", accept_multiple_files=False)
document_name = ".".join(document.name.split(".")[:-1]) if document else "Unnamed_document"

# Text inputs for agreement details
agreement_type = st.text_input("Enter agreement type")
applicable_law = st.text_input("Enter applicable law")
sector = st.text_input("Enter sector")
party = st.text_input("Enter reviewing party")

if "clauses" not in st.session_state:
    st.session_state.clauses = []

# Function to add a new clause for a party
def add_new_clause():
    st.session_state.clauses.append({"clause_number": "", "clause_text": "", "clause_correction": "", "comment": ""})

# Function to delete a clause for a party
def delete_clause(clause_index):
    st.session_state.clauses.pop(clause_index)

# Button to add a new clause for this party
if st.button(f"Add clause", key=f"add_clause"):
    add_new_clause()

# Display clause inputs for this party
for j, clause in enumerate(st.session_state.clauses):
    st.session_state.clauses[j]["clause_number"] = st.text_input(f"Clause {j + 1} Number", value=clause["clause_number"], key=f"clause_{j}_number")
    st.session_state.clauses[j]["clause_text"] = st.text_area(f"Clause {j + 1} Text", value=clause["clause_text"], key=f"clause_{j}_text")
    st.session_state.clauses[j]["clause_correction"] = st.text_area(f"Clause {j + 1} Correction", value=clause["clause_correction"], key=f"clause_{j}_correction")
    st.session_state.clauses[j]["comment"] = st.text_input(f"Clause {j + 1} Comment", value=clause["comment"], key=f"clause_{j}_comment")
    if st.button(f"Delete Clause {j + 1}", key=f"delete_clause_{j}"):
        delete_clause(j)
        st.experimental_rerun()

# Function to create the JSON data
def create_json_file():
    data = {
        "title": document_name,
        "agreement_type": agreement_type,
        "applicable_law": applicable_law,
        "sector": sector,
        "corrections": []
    }

    for clause in st.session_state.clauses:
        clause_data = {
            "clause_no": clause["clause_number"],
            "clause_text": clause["clause_text"],
            "clause_correction": clause["clause_correction"],
            "comment": clause["comment"]
        }
        data["corrections"].append(clause_data)

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
