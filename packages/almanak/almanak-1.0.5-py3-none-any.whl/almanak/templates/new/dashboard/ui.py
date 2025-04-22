import streamlit as st

# ================================================================
#                       SESSION VARIABLES
# ================================================================
if "config" not in st.session_state:
    st.session_state["config"] = None

if "initialized" not in st.session_state:
    st.session_state["initialized"] = False

if "admin_mode" not in st.session_state:
    st.session_state["admin_mode"] = False


# ================================================================
#                         STREAMLIT APP
# ================================================================
st.title("New Almanak Dashboard")
