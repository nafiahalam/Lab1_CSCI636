import requests
import json
from bs4 import BeautifulSoup


def extract_bio(data):
    teacher_bio = {}
    if data: 
        teacher_bio["Name"] = data.h3.get_text()
        teacher_bio["Bio"] = data.p.get_text()
        bio_fields = data.p.get_text().split(" ")
        try:
            teacher_bio["Courses"] = data.p.get_text()[data.p.get_text().find("Specialty:"): data.p.get_text().find("Educational")].split(":")[1]
        except TypeError as e:
            teacher_bio["Courses"] = ""
        except IndexError as e:
            teacher_bio["Courses"] = ""
        try:
            bio_url = bio_fields[bio_fields.index("Page:") + 1]
        except ValueError as e:
            bio_url = ""
        teacher_bio["Bio_Url"] = bio_url
    return teacher_bio
    

r = requests.get("https://www.hunter.cuny.edu/csci/people/faculty")
soup = BeautifulSoup(r.content, 'html.parser')

teacher_bios = []
bio_urls = []
courses = []
teachers = soup.body.table.tbody.tr.find_all("tr")

for index in range(len(teachers)):
    try:
        teacher = extract_bio(teachers[index])

        bio_urls.append(teacher["Bio_Url"])
        courses.append(teacher["Courses"])
        teacher_bios.append(teacher)
    except AttributeError as e:
        print(e)
        print(teachers[index])

with open("bios.txt", "w") as f:
    f.write(json.dumps(teacher_bios))

with open("bio_urls.txt", "w") as f:
    f.write(json.dumps(bio_urls))

with open("courses_taught.txt", "w") as f:
    f.write(json.dumps(courses))

    