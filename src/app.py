'''
TODO: add support for credit hours, days met for filtering
TODO: add support for displaying sections, professors, dates, times, and locations in a table
'''

from search.search_functions import (
    retrieve_data,
    get_search_embedding,
    get_similarities,
)

import streamlit as st
from enum import Enum 

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
        background-color: #222222;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
        padding: 15px;
        margin-bottom: 15px;
    }
</style>
"""

CARD_CONTENT = """
<a style='text-decoration: none; color: inherit;'>
    <div class="card">
        <h3>{course_id} | {course_name}</h3>
        <p>{course_description}</p>
    </div>
</a>
"""


def reset(): 
    pass

def display_results(result):

    course_name = result.get("Course Name")
    course_id = result.get("Course ID")
    course_description = result.get("Course Description")

    result_card = CARD_CONTENT.format(
        course_name=course_name,
        course_id=course_id,
        course_description=course_description,
    )
    st.markdown(DISPLAY_CARD_STYLE, unsafe_allow_html=True)
    st.markdown(result_card, unsafe_allow_html=True)

def main(): 
    st.markdown(TITLE, unsafe_allow_html=True)
    st.markdown(SUBHEADING, unsafe_allow_html=True)

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
        df = retrieve_data()

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
    main()