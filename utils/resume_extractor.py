import re



def extract_resume_details(text):


    data = {


        "name":"",

        "email":"",

        "phone":"",

        "job_title":"",

        "skills":"",

        "summary":"",

        "experience":"",

        "education":""


    }



    # Email


    email = re.search(

        r'[\w\.-]+@[\w\.-]+',

        text

    )


    if email:

        data["email"] = email.group()



    # Phone


    phone = re.search(

        r'\b\d{10}\b',

        text

    )


    if phone:

        data["phone"] = phone.group()



    lines = text.split("\n")



    clean_lines=[

        x.strip()

        for x in lines

        if x.strip()

    ]



    # First line as name


    if len(clean_lines)>0:

        data["name"]=clean_lines[0]



    # Summary


    data["summary"] = text[:600]



    # Skills detection


    skills=[


    "python",

    "java",

    "sql",

    "excel",

    "cobol",

    "jcl",

    "mainframe",

    "aws",

    "javascript"


    ]



    found=[]



    lower=text.lower()



    for s in skills:


        if s in lower:

            found.append(s)



    data["skills"]=", ".join(found)



    # Experience


    data["experience"]=text



    return data