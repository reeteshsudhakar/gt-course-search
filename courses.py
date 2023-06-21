import requests
import json
import pandas as pd

CURRENT_TERM = "202308"
DATA_LINK = f"https://raw.githubusercontent.com/gt-scheduler/crawler-v2/gh-pages/{CURRENT_TERM}.json"

response = requests.get(DATA_LINK)
data = json.loads(response.text)

del data["caches"]
del data["updatedAt"]
del data["version"]

'''
key: course ID (str)
value: List
    0: course name
    1: Dict
        key: section letter (str) 
        value: List
            0: CRN (str) 
            1: List
                1: days met (str)
                2: location (str)
                4: List
                    0: professor (str)
    2: 
    3: course description (str) 
'''

courses = data["courses"]
for key, value in courses.items(): 
    print(key) # course ID
    print(value[0]) # course name
    for section, info in value[1].items():
        print(section) # section letter
        print(info[0]) # CRN
        print(info[1][0][1]) # days met
        print(info[1][0][2]) # location
        print(info[1][0][4][0]) # professor