from docx import Document
import tempfile
import os
import re



def replace_text(doc, mapping):


    for paragraph in doc.paragraphs:


        for key,value in mapping.items():


            if key in paragraph.text:


                paragraph.text = paragraph.text.replace(

                    key,

                    value

                )




    for table in doc.tables:


        for row in table.rows:


            for cell in row.cells:


                for paragraph in cell.paragraphs:


                    for key,value in mapping.items():


                        if key in paragraph.text:


                            paragraph.text = paragraph.text.replace(

                                key,

                                value

                            )





def remove_unused_placeholders(doc):


    pattern=r"\{\{.*?\}\}"



    for paragraph in doc.paragraphs:


        if re.search(pattern,paragraph.text):


            paragraph.text=re.sub(

                pattern,

                "",

                paragraph.text

            )




    for table in doc.tables:


        for row in table.rows:


            for cell in row.cells:


                for paragraph in cell.paragraphs:


                    paragraph.text=re.sub(

                        pattern,

                        "",

                        paragraph.text

                    )







def create_mapping(data):


    mapping={



    "{{NAME}}":
    data.get("name",""),



    "{{JOB_TITLE}}":
    data.get("job_title",""),



    "{{EMAIL}}":
    data.get("email",""),



    "{{PHONE}}":
    data.get("phone",""),



    "{{LOCATION}}":
    data.get("location",""),



    "{{LINKEDIN}}":
    data.get("linkedin",""),



    "{{GITHUB}}":
    data.get("github",""),



    "{{SUMMARY}}":
    data.get("summary",""),



    "{{SKILLS}}":
    ", ".join(data.get("skills",[]))

    }



    # Experience


    experiences=data.get(

        "experience",

        []

    )


    for index,exp in enumerate(experiences,start=1):


        bullets="\n".join(

            exp.get(

                "responsibilities",

                []

            )

        )



        mapping.update({



        f"{{{{EXPERIENCE.{index}.ROLE}}}}":

        exp.get("role",""),



        f"{{{{EXPERIENCE.{index}.COMPANY}}}}":

        exp.get("company",""),



        f"{{{{EXPERIENCE.{index}.DURATION}}}}":

        exp.get("duration",""),



        f"{{{{EXPERIENCE.{index}.RESPONSIBILITIES}}}}":

        bullets



        })





    # Projects


    for index,p in enumerate(

        data.get("projects",[]),

        start=1

    ):



        mapping.update({



        f"{{{{PROJECTS.{index}.NAME}}}}":

        p.get("name",""),



        f"{{{{PROJECTS.{index}.DESCRIPTION}}}}":

        p.get("description","")



        })



    return mapping







def create_docx(template_name,data):



    template=os.path.join(

        "templates",

        template_name

    )



    doc=Document(template)



    mapping=create_mapping(data)



    replace_text(

        doc,

        mapping

    )



    remove_unused_placeholders(

        doc

    )



    output=tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".docx"

    )



    doc.save(

        output.name

    )



    return output.name
