import re
from docx import Document



def extract_resume_text(file):

    doc = Document(file)

    text=[]


    for p in doc.paragraphs:

        if p.text.strip():

            text.append(p.text)



    for table in doc.tables:

        for row in table.rows:

            for cell in row.cells:

                text.append(cell.text)



    return "\n".join(text)





def find_section(text, title, next_sections):


    pattern = (
        title +
        r"(.*?)(?="
        +
        "|".join(next_sections)
        +
        "|$)"
    )


    match=re.search(

        pattern,

        text,

        re.I|re.S

    )


    if match:

        return match.group(1).strip()


    return ""







def parse_resume(text):


    data={}



    lines=[

        x.strip()

        for x in text.split("\n")

        if x.strip()

    ]



    # NAME

    data["name"]=lines[0] if lines else ""




    # EMAIL

    email=re.findall(

        r'\S+@\S+',

        text

    )


    data["email"]=email[0] if email else ""




    # PHONE

    phone=re.findall(

        r'\+?\d[\d\s-]{8,}',

        text

    )


    data["phone"]=phone[0] if phone else ""





    # LINKS

    data["linkedin"]=""

    data["github"]=""





    # SKILLS

    skill_section=find_section(

        text,

        "SKILLS",

        [

        "EXPERIENCE",

        "EDUCATION",

        "PROJECTS"

        ]

    )


    data["skills"]=[

        x.strip()

        for x in skill_section.replace(

            ",",

            "\n"

        ).split("\n")

        if x.strip()

    ]







    # SUMMARY

    summary=find_section(

        text,

        "SUMMARY",

        [

        "SKILLS",

        "EXPERIENCE"

        ]

    )


    data["summary"]=summary





    # EDUCATION


    edu=find_section(

        text,

        "EDUCATION",

        [

        "EXPERIENCE",

        "PROJECTS"

        ]

    )



    edu_lines=[

        x.strip()

        for x in edu.split("\n")

        if x.strip()

    ]


    data["education"]=[

        {

        "degree":

        edu_lines[0] if len(edu_lines)>0 else "",


        "university":

        edu_lines[1] if len(edu_lines)>1 else "",


        "year":

        edu_lines[2] if len(edu_lines)>2 else ""

        }

    ]







    # EXPERIENCE


    exp=find_section(

        text,

        "EXPERIENCE",

        [

        "EDUCATION",

        "PROJECTS",

        "CERTIFICATIONS"

        ]

    )


    exp_lines=[

        x.strip()

        for x in exp.split("\n")

        if x.strip()

    ]



    bullets=[

        x.replace(

            "•",

            ""

        ).replace(

            "-",

            ""

        )

        for x in exp_lines

        if x.startswith(("•","-"))

    ]



    data["experience"]=[

        {

        "role":

        exp_lines[0] if len(exp_lines)>0 else "",


        "company":

        exp_lines[1] if len(exp_lines)>1 else "",


        "location":"",


        "dates":"",


        "bullet1":

        bullets[0] if len(bullets)>0 else "",


        "bullet2":

        bullets[1] if len(bullets)>1 else "",


        "bullet3":

        bullets[2] if len(bullets)>2 else ""

        }

    ]







    # PROJECTS


    projects=find_section(

        text,

        "PROJECTS",

        [

        "CERTIFICATION",

        "SKILLS"

        ]

    )


    data["projects"]=[

        {

        "name":

        projects.split("\n")[0]
        if projects else "",


        "description":

        projects,


        "link":""

        }

    ]






    # CERTIFICATIONS


    cert=find_section(

        text,

        "CERTIFICATION",

        [

        "PROJECT"

        ]

    )


    data["certifications"]=cert.split("\n") if cert else []




    # ACHIEVEMENTS


    ach=find_section(

        text,

        "ACHIEVEMENTS",

        [

        "PROJECT"

        ]

    )


    data["achievements"]=ach.split("\n") if ach else []



    return data
