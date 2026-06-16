from docx import Document
import os
import tempfile



def replace_paragraph(paragraph, mapping):

    full_text = ""

    for run in paragraph.runs:
        full_text += run.text


    updated = full_text


    for key,value in mapping.items():

        if value is None:
            value = ""

        updated = updated.replace(
            key,
            str(value)
        )


    if updated != full_text:


        for run in paragraph.runs:
            run.text=""


        if paragraph.runs:
            paragraph.runs[0].text = updated




def replace_table(table,mapping):


    for row in table.rows:

        for cell in row.cells:

            for paragraph in cell.paragraphs:

                replace_paragraph(
                    paragraph,
                    mapping
                )





def build_mapping(data):


    mapping={}



    # Simple fields

    for key,value in data.items():


        if not isinstance(value,(list,dict)):


            mapping[

            "{{"+key.upper()+"}}"

            ] = value




    # Skills

    mapping["{{SKILLS}}"] = ", ".join(

        data.get(
            "skills",
            []

        )

    )




    # Education


    for i,item in enumerate(

        data.get("education",[]),

        1

    ):


        for k,v in item.items():


            mapping[

            f"{{{{EDUCATION.{i}.{k.upper()}}}}}"

            ] = v




    # Experience


    for i,item in enumerate(

        data.get("experience",[]),

        1

    ):


        for k,v in item.items():


            mapping[

            f"{{{{EXPERIENCE.{i}.{k.upper()}}}}}"

            ] = v




    # Projects


    for i,item in enumerate(

        data.get("projects",[]),

        1

    ):


        for k,v in item.items():


            mapping[

            f"{{{{PROJECTS.{i}.{k.upper()}}}}}"

            ] = v





    # Achievements


    mapping["{{ACHIEVEMENTS}}"] = "\n".join(

        data.get(

            "achievements",

            []

        )

    )




    # Certifications


    mapping["{{CERTIFICATIONS}}"] = "\n".join(

        data.get(

            "certifications",

            []

        )

    )



    return mapping






def create_docx(template_name,resume_data):


    template_path=os.path.join(

        "templates",

        template_name

    )


    if not os.path.exists(template_path):

        raise FileNotFoundError(
            template_path
        )



    doc=Document(

        template_path

    )



    mapping=build_mapping(

        resume_data

    )



    for paragraph in doc.paragraphs:

        replace_paragraph(

            paragraph,

            mapping

        )



    for table in doc.tables:

        replace_table(

            table,

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
