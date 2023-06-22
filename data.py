import requests
import json
import csv

CURRENT_TERM = "202308"
DATA_LINK = f"https://raw.githubusercontent.com/gt-scheduler/crawler-v2/gh-pages/{CURRENT_TERM}.json"

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

def process_data(): 
    response = requests.get(DATA_LINK)
    data = json.loads(response.text)

    del data["caches"]
    del data["updatedAt"]
    del data["version"]

    courses = data["courses"]
    fields = ["Course ID", "Course Name", "Section Letters", "CRNs", "Days Met", "Locations", "Professors", "Course Description"]

    with open("courses.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        for course_id, course_data in courses.items(): 
            # print(key) # course ID
            # print(value[0]) # course name
            crns, section_letters, days_met_list, locations, professors = [], [], [], [], []
            for section_letter, info in course_data[1].items():
                # print(section) # section letter
                # print(info[0]) # CRN
                # print(info[1][0][1]) # days met
                # print(info[1][0][2]) # location
                # print(info[1][0][4][0]) # professor

                crn, days_met, location, professor = "", "", "", ""

                try: 
                    crn = info[0]
                except: 
                    crn = ""
                
                try:
                    days_met = info[1][0][1]
                except:
                    days_met = ""

                try:
                    location = info[1][0][2]
                except:
                    location = ""

                try:
                    professor = info[1][0][4][0]
                except:
                    professor = ""
                
                crns.append(crn if crn else "")
                section_letters.append(section_letter)
                days_met_list.append(days_met if days_met else "")
                locations.append(location if location else "")
                professors.append(professor if professor else "")

            crns_to_string = ";".join(crns)
            section_letters_to_string = ";".join(section_letters)
            days_met_to_string = ";".join(days_met_list)
            locations_to_string = ";".join(locations)
            professors_to_string = ";".join(professors)
            course_name = course_data[0]
            course_description = course_data[3]

            data_to_write = [course_id, 
                            course_name, 
                            section_letters_to_string, 
                            crns_to_string, 
                            days_met_to_string, 
                            locations_to_string, 
                            professors_to_string, 
                            course_description
                            ]
            
            writer.writerow(data_to_write)
        
        f.close()


if __name__ == "__main__":
    process_data()