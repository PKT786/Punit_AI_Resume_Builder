import re



def calculate_ats_score(resume_text, job_description=""):


    score = 0


    suggestions=[]



    text = resume_text.lower()



    # ---------------------
    # Contact Information
    # ---------------------


    if "email" in text or "@" in text:

        score +=10

    else:

        suggestions.append(
        "Add professional email address"
        )



    if "phone" in text or re.search(r'\d{10}',text):

        score +=10

    else:

        suggestions.append(
        "Add phone number"
        )



    # ---------------------
    # Skills Section
    # ---------------------


    skills=[

    "python",

    "sql",

    "excel",

    "java",

    "aws",

    "cobol",

    "jcl",

    "mainframe"

    ]



    found=[]



    for skill in skills:


        if skill in text:


            found.append(skill)



    if len(found)>=3:


        score+=20


    else:


        suggestions.append(

        "Add more technical skills"

        )



    # ---------------------
    # Experience
    # ---------------------


    if "experience" in text:


        score+=15


    else:


        suggestions.append(

        "Add work experience section"

        )



    # ---------------------
    # Education
    # ---------------------


    if "education" in text:


        score+=10


    else:


        suggestions.append(

        "Add education details"

        )



    # ---------------------
    # Keywords
    # ---------------------


    if job_description:


        keywords = job_description.lower().split()


        matches=0


        for k in keywords:


            if k in text:


                matches+=1



        score += min(

            matches,

            35

        )



    else:


        score +=15



    return {


    "score":

    min(score,100),


    "skills_found":

    found,


    "suggestions":

    suggestions


    }