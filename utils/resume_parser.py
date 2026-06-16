from docx import Document
import re



def extract_resume_text(file):

    doc = Document(file)

    content = []


    for p in doc.paragraphs:

        if p.text.strip():

            content.append(
                p.text.strip()
            )


    for table in doc.tables:

        for row in table.rows:

            row_text = []

            for cell in row.cells:

                row_text.append(
                    cell.text.strip()
                )


            content.append(
                " ".join(row_text)
            )


    return "\n".join(content)





def clean_list(items):

    result=[]

    for item in items:

        item=item.strip()

        item=item.replace(
            "•",
            ""
        )

        item=item.replace(
            "-",
            ""
        )


        if item:

            result.append(item)


    return result





def extract_email(text):

    match=re.findall(
        r'\S+@\S+',
        text
    )

    return match[0] if match else ""





def extract_phone(text):

    match=re.findall(

        r'(\+?\d[\d\s\-]{8,})',

        text

    )

    return match[0] if match else ""





def extract_links(text):

    links=re.findall(

        r'https?://\S+',

        text

    )

    linkedin=""

    github=""


    for link in links:


        if "linkedin" in link.lower():

            linkedin=link


        if "github" in link.lower():

            github=link



    return linkedin,github





def find_section(text, keywords):


    lines=text.split("\n")


    start=False

    data=[]


    for line in lines:


        low=line.lower()



        if any(

            k.lower() in low

            for k in keywords

        ):

            start=True

            continue



        if start:


            if line.isupper():

                break


            data.append(line)



    return data





def parse_resume(text):


    lines=[

        x.strip()

        for x in text.split("\n")

        if x.strip()

    ]



    data={}



    # NAME

    data["name"] = lines[0] if lines else ""



    # Contact


    data["email"]=extract_email(text)

    data["phone"]=extract_phone(text)



    linkedin,github=extract_links(text)


    data["linkedin"]=linkedin

    data["github"]=github



    data["location"]=""




    # Job title


    title_keywords=[

        "developer",

        "engineer",

        "analyst",

        "support",

        "manager"

    ]



    data["job_title"]=""



    for line in lines[:10]:


        if any(

            k in line.lower()

            for k in title_keywords

        ):


            data["job_title"]=line

            break





    # SUMMARY


    summary=find_section(

        text,

        [

            "summary",

            "profile",

            "objective",

            "professional summary"

        ]

    )


    data["summary"]=" ".join(summary)





    # Skills


    skills=find_section(

        text,

        [

            "skills",

            "technical skills",

            "tools",

            "technology"

        ]

    )


    data["skills"]=clean_list(skills)







    # Experience


    exp_lines=find_section(

        text,

        [

            "experience",

            "professional experience",

            "work experience",

            "employment"

        ]

    )



    experience=[]


    current={}



    for line in exp_lines:



        if (

            "role:" in line.lower()

            or

            "designation:" in line.lower()

        ):


            if current:

                experience.append(current)



            current={

                "role":

                line.split(":")[-1].strip(),

                "company":"",

                "duration":"",

                "responsibilities":[]

            }



        elif "client:" in line.lower():


            current["company"]=line.split(":")[-1].strip()



        elif "duration:" in line.lower():


            current["duration"]=line.split(":")[-1].strip()



        else:


            if current:


                current["responsibilities"].append(

                    line

                )




    if current:

        experience.append(current)



    data["experience"]=experience






    # Education


    education=find_section(

        text,

        [

            "education",

            "qualification",

            "academic"

        ]

    )


    data["education"]=[

        {

            "degree":education[0] if education else "",

            "university":education[1] if len(education)>1 else "",

            "year":""

        }

    ]







    # Projects


    projects=find_section(

        text,

        [

            "project",

            "projects"

        ]

    )



    data["projects"]=[

        {

            "name":

            p,

            "description":"",

            "link":""

        }

        for p in projects

    ]






    # Certifications


    cert=find_section(

        text,

        [

            "certification",

            "certifications"

        ]

    )


    data["certifications"]=cert






    # Achievements


    data["achievements"]=find_section(

        text,

        [

            "achievement",

            "award"

        ]

    )



    return data
