import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time

st.set_page_config(layout="wide")
with open('ui.html', 'r') as f:
    html_content = f.read()
components.html(html_content, height=100) 




def main ():
    menu = ["AI","DS","ML","DA Gray","DA Black","DA white","DS6","DS7 Blue","DS7 Green"]

    st.subheader("Attendance")

    datafile = st.file_uploader("Upload CSV",type = ['csv'])
    if datafile is not None:
        df= pd.read_csv(datafile)
        st.dataframe(df)

        choice = st.selectbox("Course", menu)
        if (st.button("Update")) and choice is not None:
            progress_bar = st.progress(0)

            for percent_complete in range(100):
                time.sleep(0.001)  # Delay for each step
                progress_bar.progress(percent_complete + 1)

            st.success("Progress complete!")



if __name__ == "__main__":
    main()
