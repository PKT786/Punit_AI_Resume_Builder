from docx import Document
import tempfile
import os


def replace_all(paragraph, mapping):

    text = paragraph.text

    for key,value in mapping.items():

        if value is None:
            value=""

        text=text.replace(
            key,
            str(value)
        )


    # remove remaining placeholders

    import re

    text=re.sub(

        r"\{\{.*?\}\}",

        "",

        text

    )


    for run in paragraph.runs:

        run.text=""


    if paragraph.runs:

        paragraph.runs[0].text=text




def build_mapping(data):


    mapping={}



    # normal fields

    fields=[

        "name",
        "job_title",
        "email",
        "phone",
        "location",
        "linkedin",
        "github",
        "summary"

    ]



    for f in fields:


        mapping[

        "{{"+f.upper()+"}}"

        ]=data.get(f,"")




    mapping["{{SKILLS}}"]=", ".join(

        data.get(

            "skills",

            []

        )

    )




    # Experience

    experiences=data.get(

        "experience",

        []

    )



    for i in range(1,6):


        exp={}



        if i <= len(experiences):

            exp=experiences[i-1]



        for key in [

            "role",

            "company",

            "location",

            "dates",

            "bullet1",

            "bullet2",

            "bullet3"

        ]:


            mapping[

            f"{{{{EXPERIENCE.{i}.{key.upper()}}}}}"

            ] = exp.get(key,"")







    # Education


    edu=data.get(

        "education",

        []

    )



    first={}


    if edu:

        first=edu[0]



    for key in [

        "degree",

        "university",

        "year"

    ]:


        mapping[

        f"{{{{EDUCATION.1.{key.upper()}}}}}"

        ] = first.get(key,"")








    # Projects


    projects=data.get(

        "projects",

        []

    )



    for i in range(1,6):


        project={}


        if i <= len(projects):

            project=projects[i-1]



        for key in [

            "name",

            "description",

            "link"

        ]:


            mapping[

            f"{{{{PROJECTS.{i}.{key.upper()}}}}}"

            ] = project.get(key,"")






    mapping["{{CERTIFICATIONS}}"] = "\n".join(

        data.get(

            "certifications",

            []

        )

    )


    mapping["{{ACHIEVEMENTS}}"] = "\n".join(

        data.get(

            "achievements",

            []

        )

    )



    return mapping





def create_docx(template_name,resume_data):


    path=os.path.join(

        "templates",

        template_name

    )


    doc=Document(path)



    mapping=build_mapping(

        resume_data

    )



    for p in doc.paragraphs:


        replace_all(

            p,

            mapping

        )



    for table in doc.tables:


        for row in table.rows:


            for cell in row.cells:


                for p in cell.paragraphs:


                    replace_all(

                        p,

                        mapping

                    )



    output=tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".docx"

    )



    doc.save(

        output.name

    )



    return output.name
