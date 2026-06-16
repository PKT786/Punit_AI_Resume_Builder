from docx import Document
import re



def extract_resume_text(file):

    doc = Document(file)

    text=[]


    for p in doc.paragraphs:

        if p.text.strip():

            text.append(p.text.strip())



    for table in doc.tables:

        for row in table.rows:

            text.append(

                " ".join(

                    c.text.strip()

                    for c in row.cells

                )

            )


    return "\n".join(text)






def section_extract(text, headings):


    pattern="|".join(headings)


    match=re.search(

        rf"({pattern})(.*?)(?=\n[A-Z][A-Z\s]+$|$)",

        text,

        re.I|re.S

    )


    if match:

        return match.group(2).strip()


    return ""








def parse_resume(text):


    data={}




    lines=[

        x.strip()

        for x in text.split("\n")

        if x.strip()

    ]



    # Name


    data["name"]=lines[0]



    # Email


    email=re.findall(

        r'\S+@\S+',

        text

    )


    data["email"]=email[0] if email else ""





    # Phone


    phone=re.findall(

        r'\+?\d[\d\s-]{8,}',

        text

    )


    data["phone"]=phone[0] if phone else ""







    # Summary


    summary=section_extract(

        text,

        [

        "SUMMARY",

        "PROFESSIONAL SUMMARY",

        "PROFILE"

        ]

    )


    data["summary"]=summary







    # Skills


    skills=section_extract(

        text,

        [

        "SKILLS",

        "TECHNICAL SKILLS",

        "CORE SKILLS"

        ]

    )


    data["skills"]=[

        s.strip()

        for s in re.split(

            ",|\n|\|",

            skills

        )

        if s.strip()

    ]








    # Experience


    exp=section_extract(

        text,

        [

        "EXPERIENCE",

        "PROFESSIONAL EXPERIENCE",

        "WORK EXPERIENCE",

        "EMPLOYMENT"

        ]

    )



    exp_lines=[

        x.strip()

        for x in exp.split("\n")

        if x.strip()

    ]



    bullets=[]


    for line in exp_lines:


        if (

            line.startswith("•")

            or

            line.startswith("-")

        ):

            bullets.append(

                line.replace(

                    "•",""

                ).replace(

                    "-",""

                ).strip()

            )





    data["experience"]=[

        {

        "role":exp_lines[0] if exp_lines else "",


        "company":exp_lines[1] if len(exp_lines)>1 else "",


        "location":"",


        "dates":"",


        "bullet1":bullets[0] if len(bullets)>0 else "",


        "bullet2":bullets[1] if len(bullets)>1 else "",


        "bullet3":bullets[2] if len(bullets)>2 else ""

        }

    ]








    # Education


    edu=section_extract(

        text,

        [

        "EDUCATION",

        "ACADEMIC QUALIFICATION"

        ]

    )



    edu_lines=edu.split("\n")



    data["education"]=[

        {

        "degree":

        edu_lines[0] if edu_lines else "",


        "university":

        edu_lines[1] if len(edu_lines)>1 else "",


        "year":

        edu_lines[2] if len(edu_lines)>2 else ""

        }

    ]







    # Projects


    projects=section_extract(

        text,

        [

        "PROJECTS",

        "PROJECT"

        ]

    )



    data["projects"]=[

        {

        "name":

        projects.split("\n")[0] if projects else "",


        "description":projects,


        "link":""

        }

    ]






    # Certifications


    cert=section_extract(

        text,

        [

        "CERTIFICATION",

        "CERTIFICATIONS"

        ]

    )


    data["certifications"]=cert.split("\n") if cert else []






    # Achievements


    ach=section_extract(

        text,

        [

        "ACHIEVEMENTS",

        "ACCOMPLISHMENTS"

        ]

    )


    data["achievements"]=ach.split("\n") if ach else []





    return data
