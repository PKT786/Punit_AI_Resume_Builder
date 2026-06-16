from docx import Document
import re



def extract_resume_text(file):


    doc = Document(file)


    content=[]


    for p in doc.paragraphs:


        if p.text.strip():

            content.append(

                p.text.strip()

            )



    # tables

    for table in doc.tables:


        for row in table.rows:


            for cell in row.cells:


                content.append(

                    cell.text

                )



    return "\n".join(content)





def parse_resume(text):


    data={


        "name":"",

        "email":"",

        "phone":"",

        "location":"",

        "headline":"",

        "summary":"",

        "skills":[],

        "experience":[],

        "education":[],

        "projects":[]

    }



    lines=text.split("\n")



    clean=[

        x.strip()

        for x in lines

        if x.strip()

    ]



    # Name

    if clean:

        data["name"]=clean[0]



    # Email

    email=re.search(

        r'[\w\.-]+@[\w\.-]+',

        text

    )


    if email:

        data["email"]=email.group()



    # Phone

    phone=re.search(

        r'\d{10}',

        text

    )


    if phone:

        data["phone"]=phone.group()



    # Skills section

    skills=[

    "python",

    "java",

    "sql",

    "excel",

    "cobol",

    "jcl",

    "mainframe",

    "aws",

    "javascript",

    "react"

    ]



    for s in skills:


        if s.lower() in text.lower():

            data["skills"].append(s)



    # Complete resume as fallback

    data["summary"]=text[:800]


    data["experience"]=[text]


    return data