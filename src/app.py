from search.search_functions import (
    retrieve_data,
    get_search_embedding,
    get_similarities,
)

from enum import Enum
import streamlit as st
import pandas as pd

class CreditHours(Enum): 
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

class Level(Enum): 
    UNDERGRADUATE = "Undergraduate"
    GRADUATE = "Graduate"


class Days(Enum): 
    MONDAY = "M"
    TUESDAY = "T"
    WEDNESDAY = "W"
    THURSDAY = "R"
    FRIDAY = "F"


CREDIT_HOUR_SELECTIONS = {
    CreditHours.ONE: False,
    CreditHours.TWO: False, 
    CreditHours.THREE: False, 
    CreditHours.FOUR: False, 
}

LEVEL_SELECTIONS = {
    Level.UNDERGRADUATE: False, 
    Level.GRADUATE: False, 
}

DAYS_SELECTIONS = {
    Days.MONDAY: False, 
    Days.TUESDAY: False, 
    Days.WEDNESDAY: False, 
    Days.THURSDAY: False, 
    Days.FRIDAY: False, 
}

CURRENT_TERM = "202308"

BASE_COURSE_LINK = "https://oscar.gatech.edu/bprod/bwckctlg.p_disp_course_detail?cat_term_in={term}&subj_code_in={department}&crse_numb_in={course_number}"
CRN_SPECIFIC_LINK = "https://oscar.gatech.edu/bprod/bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}"
RMP_LINK = "https://www.ratemyprofessors.com/search/professors/361?q={professor}"

TITLE = '''
<h1 style='text-align: center;'>
    <a style='text-decoration: none; color: #B3A369;'>
        GT
    </a>
    <a style='text-decoration: none; color: inherit;'>
        Course Search
    </a>
</h1>
'''

SUBHEADING = '''
<p style='text-decoration: none; color: inherit; text-align: center; color: #E5E5E5'>
    Find your next course at Georgia Tech using an OpenAI powered search model! 🤖
</p>
'''

DISPLAY_CARD_STYLE = """
<style>
    .card {
        background-color: #343A40;
        border: 1px solid #FFFFFF;
        border-radius: 4px;
        box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .course-table {
        border-collapse: collapse;
        width: 100%;
        padding: 15px;
    }
</style>
"""

CARD_CONTENT = """
<a href={formatted_link} style='text-decoration: none; color: inherit;'>
    <div class="card">
        <h3>{course_id} | {course_name}</h3>
        <p style='text-decoration: none; color: #B3A369;'>
            Credit Hours: {credit_hours} | Level: {level}
        </p>
        <p>{course_description}</p>
        <table class="course-table">
            {table_content}
        </table>
    </div>
</a>
"""


def reset(): 
    pass

def display_results(result):

    course_name = result.get("Course Name")
    course_id = result.get("Course ID")
    course_description = result.get("Course Description")
    credit_hours = str(int(result.get("Credit Hours")))
    level = result.get("Level")

    formatted_link = BASE_COURSE_LINK.format(
        term=CURRENT_TERM,
        department=course_id.split(" ")[0],
        course_number=course_id.split(" ")[1],
    )

    table_content = "<tr><th>Section</th><th>Professor</th><th>Days</th><th>CRN</th></tr>"
    section_letters = []
    crns = []
    days_met = []
    locations = []
    professors = []
    

    for section_letter in result.get("Section Letters").split(";"):
        section_letters.append(section_letter)
    for crn in result.get("CRNs").split(";"):
        crns.append(crn)
    for location in result.get("Locations").split(";"):
        locations.append(location)
    for professor in result.get("Professors").split(";"):
        professors.append(professor)
    
    try:
        for days in result.get("Days Met").split(";"):
            days_met.append(days)
    except:
        days_met = [""] * len(section_letters)
    
    for i in range(min(len(section_letters), len(crns), len(days_met), len(locations), len(professors))):
        table_content += f"<tr><td>{section_letters[i]}</td><td><a href={RMP_LINK.format(professor='+'.join(professors[i].split(' ')[:2]))}>{professors[i]}</td><td>{days_met[i]}</td><td><a href={CRN_SPECIFIC_LINK.format(term=CURRENT_TERM, crn=crns[i])}>{crns[i]}</td></tr>"
    

    result_card = CARD_CONTENT.format(
        course_name=course_name,
        course_id=course_id,
        course_description=course_description,
        credit_hours=credit_hours,
        level=level,
        formatted_link=formatted_link,
        table_content=table_content,
    )

    st.write(DISPLAY_CARD_STYLE, unsafe_allow_html=True)
    st.write(result_card, unsafe_allow_html=True)

def main(df: pd.DataFrame):
    st.write(TITLE, unsafe_allow_html=True)
    st.write(SUBHEADING, unsafe_allow_html=True)

    with st.expander("Advanced Options"):
        st.write("Work in Progress 🚧")

        num_results = st.slider(label="Number of results to display", min_value=5, max_value=15, value=10, step=1)

        credit_hours, level, days = st.columns(3)

        credit_hours.write("Credit Hours")
        CREDIT_HOUR_SELECTIONS[CreditHours.ONE] = credit_hours.checkbox(label="1 Hour", value=CREDIT_HOUR_SELECTIONS[CreditHours.ONE])
        CREDIT_HOUR_SELECTIONS[CreditHours.TWO] = credit_hours.checkbox(label="2 Hours", value=CREDIT_HOUR_SELECTIONS[CreditHours.TWO])
        CREDIT_HOUR_SELECTIONS[CreditHours.THREE] = credit_hours.checkbox(label="3 Hours", value=CREDIT_HOUR_SELECTIONS[CreditHours.THREE])
        CREDIT_HOUR_SELECTIONS[CreditHours.FOUR] = credit_hours.checkbox(label="4 Hours", value=CREDIT_HOUR_SELECTIONS[CreditHours.FOUR])

        level.write("Level")
        LEVEL_SELECTIONS[Level.UNDERGRADUATE] = level.checkbox(label="Undergraduate", value=LEVEL_SELECTIONS[Level.UNDERGRADUATE])
        LEVEL_SELECTIONS[Level.GRADUATE] = level.checkbox(label="Graduate", value=LEVEL_SELECTIONS[Level.GRADUATE])

        days.write("Days")
        DAYS_SELECTIONS[Days.MONDAY] = days.checkbox(label="Monday", value=DAYS_SELECTIONS[Days.MONDAY])
        DAYS_SELECTIONS[Days.TUESDAY] = days.checkbox(label="Tuesday", value=DAYS_SELECTIONS[Days.TUESDAY])
        DAYS_SELECTIONS[Days.WEDNESDAY] = days.checkbox(label="Wednesday", value=DAYS_SELECTIONS[Days.WEDNESDAY])
        DAYS_SELECTIONS[Days.THURSDAY] = days.checkbox(label="Thursday", value=DAYS_SELECTIONS[Days.THURSDAY])
        DAYS_SELECTIONS[Days.FRIDAY] = days.checkbox(label="Friday", value=DAYS_SELECTIONS[Days.FRIDAY])

    search_query = st.text_input("Search for a course:", placeholder="Games 🕹️ and technology  🖥️  ...", key='search_input', on_change=reset())

    if search_query: 

        if any(CREDIT_HOUR_SELECTIONS.values()) and not all(CREDIT_HOUR_SELECTIONS.values()):
            df = df[df["Credit Hours"].isin([k.value for k, v in CREDIT_HOUR_SELECTIONS.items() if v])]
        
        if any(LEVEL_SELECTIONS.values()) and not all(LEVEL_SELECTIONS.values()):
            df = df[df["Level"].isin([k.value for k, v in LEVEL_SELECTIONS.items() if v])]
        
        if any(DAYS_SELECTIONS.values()) and all(DAYS_SELECTIONS.values()):
            df = df[df["Days Met"].str.contains("|".join([k.value for k, v in DAYS_SELECTIONS.items() if v]))]

        search_embedding = get_search_embedding(search_query)
        results = get_similarities(search_embedding, df)

        for i in range(min(num_results, results.shape[0])): 
            display_results(results.iloc[i])


if __name__ == "__main__": 
    df = retrieve_data()
    main(df=df)