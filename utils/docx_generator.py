from docx import Document
import os



def replace_all(doc,text_map):


    # paragraphs


    for p in doc.paragraphs:


        for key,value in text_map.items():


            if key in p.text:


                for run in p.runs:


                    run.text = run.text.replace(

                        key,

                        value

                    )



    # tables


    for table in doc.tables:


        for row in table.rows:


            for cell in row.cells:


                for p in cell.paragraphs:


                    for key,value in text_map.items():


                        if key in p.text:


                            p.text=p.text.replace(

                                key,

                                value

                            )



def create_docx(template,resume):


    path=os.path.join(

        "templates",

        template

    )


    doc=Document(path)



    experience="\n".join(

        resume.get(

            "experience",

            []

        )

    )



    skills=", ".join(

        resume.get(

            "skills",

            [])

    )



    education="\n".join(

        resume.get(

            "education",

            [])

    )



    mapping={



    "{{NAME}}":

    resume.get("name",""),



    "{{EMAIL}}":

    resume.get("email",""),



    "{{PHONE}}":

    resume.get("phone",""),



    "{{LOCATION}}":

    resume.get("location",""),



    "{{HEADLINE}}":

    resume.get("headline",""),



    "{{SUMMARY}}":

    resume.get("summary",""),



    "{{SKILLS}}":

    skills,



    "{{EXPERIENCE}}":

    experience,



    "{{EDUCATION}}":

    education



    }



    replace_all(

        doc,

        mapping

    )



    output="final_resume.docx"


    doc.save(output)



    return output