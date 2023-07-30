import requests
import json
import csv


CURRENT_TERM = "202308"
DATA_LINK = f"https://raw.githubusercontent.com/gt-scheduler/crawler-v2/gh-pages/{CURRENT_TERM}.json"


def safe_access(func):
    try:
        return func()
    except:
        return ""

def process_data(): 
    response = requests.get(DATA_LINK)
    data = json.loads(response.text)

    del data["caches"]
    del data["updatedAt"]
    del data["version"]

    courses = data["courses"]
    fields = [
        "Course ID", 
        "Level",
        "Course Name", 
        "Credit Hours",
        "Section Letters", 
        "CRNs", 
        "Days Met", 
        "Locations", 
        "Professors", 
        "Course Description", 
        "Full Text"
    ]

    with open("courses.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        for course_id, course_data in courses.items(): 
            sections_info = {key: [] for key in ["crns", "section_letters", "days_met_list", "locations", "professors"]}
            
            for section_letter, info in course_data[1].items():
                sections_info["crns"].append(safe_access(lambda: info[0]))
                sections_info["section_letters"].append(section_letter)
                sections_info["days_met_list"].append(safe_access(lambda: info[1][0][1]))
                sections_info["locations"].append(safe_access(lambda: info[1][0][2]))
                sections_info["professors"].append(safe_access(lambda: info[1][0][4][0]))
            
            sections_info_to_string = {key: ";".join(value) for key, value in sections_info.items()}

            course_name = course_data[0]
            course_level = "Undergraduate" if int(course_id.split(" ")[1]) < 5000 else "Graduate"
            credit_hours = list(course_data[1].values())[2]
            course_description = course_data[3]
            full_text = " ".join([course_id, course_name, course_description])

            data_to_write = [
                course_id,
                course_level,
                course_name,
                credit_hours,
                sections_info_to_string.get("section_letters", ""),
                sections_info_to_string.get("crns", ""),
                sections_info_to_string.get("days_met_list", ""),
                sections_info_to_string.get("locations", ""),
                sections_info_to_string.get("professors", ""),
                course_description,
                full_text,
            ]
            
            writer.writerow(data_to_write)


if __name__ == "__main__":
    process_data()
