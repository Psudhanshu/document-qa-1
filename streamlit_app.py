import streamlit as st
page1 = st.Page("HW1.py", title="HW1")
page2 = st.Page("HW2.py", title="HW2")
pg = st.navigation([page1,page2])
st.set_page_config(page_title="Homework Manager")
pg.run()

