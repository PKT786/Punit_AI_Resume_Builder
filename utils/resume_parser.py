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





def get_section(text,start_words,end_words):


    pattern = (

        "("

        +"|".join(start_words)

        +")(.*?)(?="

        +"|".join(end_words)

        + "|$)"

    )


    match=re.search(

        pattern,

        text,

        re.I|re.S

    )


    if match:

        return match.group(2).strip()



    return ""






def parse_resume(text):


    lines=[

        x.strip()

        for x in text.split("\n")

        if x.strip()

    ]



    data={}



    data["name"]=lines[0]




    email=re.findall(

        r'\S+@\S+',

        text

    )


    data["email"]=email[0] if email else ""




    phone=re.findall(

        r'\+?\d[\d\s-]{8,}',

        text

    )


    data["phone"]=phone[0] if phone else ""





    data["linkedin"]=""

    data["github"]=""

    data["location"]=""




    data["job_title"]="Mainframe Developer"






    summary=get_section(

        text,

        [

        "PROFESSIONAL SUMMARY"

        ],

        [

        "CORE SKILLS",

        "PROFESSIONAL EXPERIENCE"

        ]

    )


    data["summary"]=summary






    skills=get_section(

        text,

        [

        "CORE SKILLS",

        "SKILLS"

        ],

        [

        "PROFESSIONAL EXPERIENCE",

        "EDUCATION"

        ]

    )



    data["skills"]=skills.replace(

        "\n",

        ","

    )







    experience=[]



    exp=get_section(

        text,

        [

        "PROFESSIONAL EXPERIENCE",

        "EXPERIENCE"

        ],

        [

        "EDUCATION",

        "PROJECTS"

        ]

    )



    exp_lines=[

        x.strip()

        for x in exp.split("\n")

        if x.strip()

    ]



    bullets=[]



    for x in exp_lines:


        if x.startswith("•"):

            bullets.append(

                x.replace("•","")

            )





    experience.append(

        {

        "role":"Software Developer",

        "company":"",

        "dates":"",

        "location":"",

        "bullet1": bullets[0] if len(bullets)>0 else "",

        "bullet2": bullets[1] if len(bullets)>1 else "",

        "bullet3": bullets[2] if len(bullets)>2 else ""

        }

    )



    data["experience"]=experience






    project_section=get_section(

        text,

        [

        "PROJECTS"

        ],

        [

        "CERTIFICATIONS",

        "ACHIEVEMENTS"

        ]

    )



    data["projects"]=[

        {

        "name":project_section,

        "description":"",

        "link":""

        }

    ]




    data["education"]=[

        {

        "degree":"",

        "university":"",

        "year":""

        }

    ]



    data["certifications"]=[]


    data["achievements"]=[]



    return data
