import streamlit as st

st.title("Formulario de registro")

with st.form("formulario_registro"):
    id = st.text_input("Id ")
    nombre = st.text_input("Nombre")

    insertar = st.form_submit_button("Insertar")
    start = st.form_submit_button("Start")
    commit = st.form_submit_button("Commit")
    roll = st.form_submit_button("Rollback")