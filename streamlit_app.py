import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import numpy as np
from datetime import datetime
import re

st.set_page_config(layout="wide")
with open('ui.html', 'r') as f:
    html_content = f.read()
components.html(html_content, height=100) 


col1,col2 = st.columns(2)

def parse_duration(duration_str):
    minutes = 0
    hours_match = re.search(r'(\d+)\s*hr', duration_str)
    minutes_match = re.search(r'(\d+)\s*min', duration_str)
    if hours_match:
        hours = int(hours_match.group(1))
        minutes += hours * 60
    if minutes_match:
        minutes += int(minutes_match.group(1))
    return minutes


def main ():
    # available files (can be changed later)
    menu = ["AI","DS","ML","DA Gray","DA Black","DA white","DS6","DS7 Blue","DS7 Green"]

    col1.subheader("Attendance")

    datafile = col1.file_uploader("Upload CSV",type = ['csv'])
    # loading data if file is uploaded.
    if datafile is not None:
        df= pd.read_csv(datafile)
        col1.dataframe(df) # confirming that the right file is uploaded
        # choosing from the daily file.
        choice = col1.selectbox("Course", menu)
        current_date = col1.date_input("Enter the date",format="DD-MM-YYYY")
        if (st.button("Update")) and choice is not None:

            if choice == "DA Black" :
                original_df = pd.read_csv(r"C:\Users\Azeem\OneDrive\Documents\Projects\attendance_merger\DA Cohort 01(Black) - Trackerrr.csv")
                
                #######################processing the data######################
                df["Name"] = (df['First name'] + df['Last name']).str.replace(' ', '').str.lower() 
                # making it lower case to avoid erros 
                original_df['Name_lower'] = original_df['Name'].str.replace(' ', '').str.lower() # removing spaces

                #updating the duration column for the time the student attended the class
                df['Duration'] =df['Duration'].apply(parse_duration)

                original_df['duration'] = df['Duration']
                # updating the attendance with 1 for present and 0 for absent
                original_df[current_date] = np.where(original_df['Name_lower'].isin(df[df['Duration'] >= 45]['Name']),1,0)

                # dropping the extra name column and keeping the original 
                original_df.drop(columns=['Name_lower'], inplace=True)
                
                col1.dataframe(original_df) 
            st.success("Progress complete!")



if __name__ == "__main__":
    main()
