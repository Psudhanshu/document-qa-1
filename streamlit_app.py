import streamlit as st
page1 = st.Page("HW1.py", title="HW1")
page2 = st.Page("HW2.py", title="HW2")
page3 = st.Page("HW3.py", title="HW3")
page4 = st.Page("HW3_alt.py", title="HW3_alt")
pg = st.navigation([page1,page2,page3,page4])
st.set_page_config(page_title="Homework Manager")
pg.run()

