import streamlit as st
page1 = st.Page("HW1.py", title="HW1")
page2 = st.Page("HW2.py", title="HW2")
page3 = st.Page("HW3.py", title="HW3")
page4 = st.Page("HW3_alt.py", title="HW3_alt")
page5 = st.Page("HW4.py", title = "HW4.py")
page6 = st.Page("HW5.py", title = "HW5.py")
pg = st.navigation([page1,page2,page3,page4,page5,page6])
st.set_page_config(page_title="Homework Manager")
pg.run()

