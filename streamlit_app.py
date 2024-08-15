import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import numpy as np
from datetime import datetime
import re
import File_handling as fl
from io import StringIO

st.set_page_config(layout="wide")
with open('ui.html', 'r') as f:
    html_content = f.read()
components.html(html_content, height=100) 

#accessing the api key here 
GITHUB_TOKEN = st.secrets["GitHub"]["apikey"]
REPO = "AzeemChaudhry/attendance_merger"
BRANCH = "main"

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
        if st.button("Update") and choice is not None:
            # Define URLs for the online files
            urls = {
                "DA Black": "DA%20Cohort%2001(Black)%20-%20Trackerrr.csv",
                "DA Gray": "DA%20Cohort%2001(Gray)%20-%20Tracker%20-%20Attendence.csv",
                "DA White": "DA%20Cohort%2001(White)%20-%20Tracker.csv",
                "DS6": "DS%20Cohort%2006%20-%20Tracker.csv",
                "DS7 Blue": "DS%20Cohort%2007(Blue)%20-%20Tracker.csv",
                "DS7 Green": "DS%20Cohort%2007(Green)%20-%20Tracker.csv"
            }
            
            if choice in urls:
                try:
                    file_path = urls[choice]
                    original_content, sha = fl.get_file_content(file_path)
                    original_df = pd.read_csv(StringIO(original_content))
                    #######################processing the data######################
                    df["Name"] = (df['First name'] + df['Last name']).str.replace(' ', '').str.lower() 
                    # making it lower case to avoid erros 
                    original_df['Name_lower'] = original_df['Name'].str.replace(' ', '').str.lower() # removing spaces

                    #updating the duration column for the time the student attended the class
                    df['duration'] =df['Duration'].apply(parse_duration)

                    original_df['duration'] = df['duration']
                    # updating the attendance with 1 for present and 0 for absent
                    original_df[current_date] = np.where(original_df['Name_lower'].isin(df[df['duration'] >= 45]['Name']),1,0)

                    # dropping the extra name column and keeping the original 
                    original_df.drop(columns=['Name_lower'], inplace=True)
                    df.drop(columns=['duration'], inplace=True)
                    original_df.drop(columns=['duration'], inplace=True)
                    df.drop(columns=['Name'], inplace=True)

                    # Update the file on GitHub
                    updated_content = original_df.to_csv(index=False)
                    fl.update_file(file_path, updated_content, sha)
                    
                    col1.dataframe(original_df) 
                    st.success("Done ✔️")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Error: Could not find the course file")



if __name__ == "__main__":
    main()
