import re
from docx import Document




# --------------------------------------------------
# Extract complete text from DOCX
# --------------------------------------------------

def extract_resume_text(file):


    doc = Document(file)



    content = []



    # Paragraphs

    for paragraph in doc.paragraphs:


        if paragraph.text.strip():


            content.append(

                paragraph.text.strip()

            )



    # Tables

    for table in doc.tables:


        for row in table.rows:


            row_text=[]


            for cell in row.cells:


                row_text.append(

                    cell.text.strip()

                )


            content.append(

                " ".join(row_text)

            )



    return "\n".join(content)







# --------------------------------------------------
# Email
# --------------------------------------------------

def extract_email(text):


    result = re.findall(

        r'[\w\.-]+@[\w\.-]+',

        text

    )


    return result[0] if result else ""






# --------------------------------------------------
# Phone
# --------------------------------------------------

def extract_phone(text):


    result = re.findall(

        r'(\+?\d[\d\s\-]{8,15})',

        text

    )


    return result[0] if result else ""







# --------------------------------------------------
# LinkedIn
# --------------------------------------------------

def extract_linkedin(text):


    match = re.search(

        r'https?://(?:www\.)?linkedin\.com/[^\s]+',

        text,

        re.I

    )


    return match.group(0) if match else ""






# --------------------------------------------------
# Github
# --------------------------------------------------

def extract_github(text):


    match = re.search(

        r'https?://(?:www\.)?github\.com/[^\s]+',

        text,

        re.I

    )


    return match.group(0) if match else ""







# --------------------------------------------------
# Skills
# --------------------------------------------------

def extract_skills(text):


    skills=[]


    keywords=[


        "Python",

        "Java",

        "SQL",

        "Excel",

        "Power BI",

        "Tableau",

        "COBOL",

        "JCL",

        "Mainframe",

        "AWS",

        "Azure",

        "AI",

        "Machine Learning",

        "HTML",

        "CSS",

        "JavaScript"

    ]



    for skill in keywords:


        if skill.lower() in text.lower():


            skills.append(skill)



    return skills








# --------------------------------------------------
# Section Extractor
# --------------------------------------------------

def get_section(text,start,end_list):


    text_upper=text.upper()


    start_pos=text_upper.find(

        start

    )



    if start_pos == -1:


        return ""



    content=text[start_pos + len(start):]



    for end in end_list:


        pos=content.upper().find(end)



        if pos!=-1:


            content=content[:pos]

            break



    return content.strip()







# --------------------------------------------------
# Education
# --------------------------------------------------

def extract_education(text):


    section=get_section(

        text,

        "EDUCATION",

        [

            "EXPERIENCE",

            "SKILLS",

            "PROJECTS",

            "CERTIFICATION"

        ]

    )



    if not section:


        return [

            {

            "degree":"",

            "university":"",

            "year":""

            }

        ]



    lines=[

        x.strip()

        for x in section.split("\n")

        if x.strip()

    ]



    return [

        {

        "degree": lines[0] if len(lines)>0 else "",

        "university": lines[1] if len(lines)>1 else "",

        "year": lines[2] if len(lines)>2 else ""

        }

    ]







# --------------------------------------------------
# Experience
# --------------------------------------------------

def extract_experience(text):


    section=get_section(

        text,

        "EXPERIENCE",

        [

            "EDUCATION",

            "PROJECTS",

            "CERTIFICATION",

            "ACHIEVEMENTS"

        ]

    )



    if not section:


        return [

            {

            "role":"",

            "company":"",

            "location":"",

            "dates":"",

            "bullet1":"",

            "bullet2":"",

            "bullet3":""

            }

        ]



    lines=[

        x.strip()

        for x in section.split("\n")

        if x.strip()

    ]



    bullets=[]


    for line in lines:


        if line.startswith("-") or line.startswith("•"):


            bullets.append(

                line.replace(

                    "-",

                    ""

                ).replace(

                    "•",

                    ""

                ).strip()

            )



    return [

        {

        "role":lines[0] if len(lines)>0 else "",

        "company":lines[1] if len(lines)>1 else "",

        "location":"",

        "dates":"",

        "bullet1":bullets[0] if len(bullets)>0 else "",

        "bullet2":bullets[1] if len(bullets)>1 else "",

        "bullet3":bullets[2] if len(bullets)>2 else ""

        }

    ]







# --------------------------------------------------
# Projects
# --------------------------------------------------

def extract_projects(text):


    section=get_section(

        text,

        "PROJECTS",

        [

            "CERTIFICATION",

            "ACHIEVEMENT",

            "SKILLS"

        ]

    )



    if not section:


        return [

            {

            "name":"",

            "link":"",

            "description":""

            }

        ]



    lines=[

        x.strip()

        for x in section.split("\n")

        if x.strip()

    ]



    return [

        {

        "name":lines[0] if len(lines)>0 else "",

        "link":"",

        "description":" ".join(lines[1:])

        }

    ]








# --------------------------------------------------
# Certifications
# --------------------------------------------------

def extract_certifications(text):


    section=get_section(

        text,

        "CERTIFICATION",

        [

            "PROJECTS",

            "ACHIEVEMENTS"

        ]

    )



    if not section:


        return []



    return [

        x.strip()

        for x in section.split("\n")

        if x.strip()

    ]








# --------------------------------------------------
# Achievements
# --------------------------------------------------

def extract_achievements(text):


    section=get_section(

        text,

        "ACHIEVEMENTS",

        [

            "PROJECTS",

            "CERTIFICATION"

        ]

    )


    if not section:


        return []



    return [

        x.strip()

        for x in section.split("\n")

        if x.strip()

    ]








# --------------------------------------------------
# Main Parser
# --------------------------------------------------

def parse_resume(text):


    data={}



    lines=text.split("\n")



    # Name

    data["name"] = (

        lines[0].strip()

        if lines

        else ""

    )



    data["email"]=extract_email(text)



    data["phone"]=extract_phone(text)



    data["linkedin"]=extract_linkedin(text)



    data["github"]=extract_github(text)



    data["skills"]=extract_skills(text)



    data["summary"]=text[:600]



    data["education"]=extract_education(text)



    data["experience"]=extract_experience(text)



    data["projects"]=extract_projects(text)



    data["certifications"]=extract_certifications(text)



    data["achievements"]=extract_achievements(text)



    return data
