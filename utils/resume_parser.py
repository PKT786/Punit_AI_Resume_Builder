import re
from docx import Document



def extract_resume_text(file):


    doc = Document(file)


    text=[]


    for p in doc.paragraphs:


        text.append(
            p.text
        )


    for table in doc.tables:


        for row in table.rows:


            for cell in row.cells:


                text.append(
                    cell.text
                )


    return "\n".join(text)





def parse_resume(text):


    resume={}



    # NAME

    lines=text.split("\n")


    resume["name"]=lines[0] if lines else ""



    # EMAIL

    email=re.findall(

        r'[\w\.-]+@[\w\.-]+',

        text

    )


    resume["email"]=email[0] if email else ""




    # PHONE

    phone=re.findall(

        r'\+?\d[\d -]{8,}',

        text

    )


    resume["phone"]=phone[0] if phone else ""




    # SKILLS

    skills=[]


    if "SKILLS" in text.upper():


        block=text.upper().split(

            "SKILLS"

        )[1]


        skills=block.split("\n")[0].split(",")



    resume["skills"]=[

        s.strip()

        for s in skills

        if s.strip()

    ]




    # SUMMARY

    resume["summary"]=text[:500]





    # EDUCATION

    resume["education"]=[

        {

        "degree":"",

        "university":"",

        "year":""

        }

    ]





    # EXPERIENCE

    resume["experience"]=[

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





    # ACHIEVEMENTS


    resume["achievements"]=[

        "ITIL Certified"

    ]





    # CERTIFICATION


    resume["certifications"]=[

        ""

    ]




    # PROJECTS


    resume["projects"]=[

        {

        "name":"",

        "link":"",

        "description":""

        }

    ]



    return resume
