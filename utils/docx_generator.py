from docx import Document
import os



def replace_in_paragraph(paragraph, replacements):


    full_text = ""


    for run in paragraph.runs:

        full_text += run.text



    updated = full_text



    for key,value in replacements.items():


        if key in updated:


            updated = updated.replace(

                key,

                value

            )



    if updated != full_text:


        for run in paragraph.runs:

            run.text = ""


        if paragraph.runs:

            paragraph.runs[0].text = updated



def replace_in_table(table, replacements):


    for row in table.rows:


        for cell in row.cells:


            for paragraph in cell.paragraphs:


                replace_in_paragraph(

                    paragraph,

                    replacements

                )



def replace_all(doc, replacements):


    # normal paragraphs

    for paragraph in doc.paragraphs:


        replace_in_paragraph(

            paragraph,

            replacements

        )



    # tables

    for table in doc.tables:


        replace_in_table(

            table,

            replacements

        )



    # headers

    for section in doc.sections:


        header = section.header


        for paragraph in header.paragraphs:


            replace_in_paragraph(

                paragraph,

                replacements

            )



def create_docx(resume_data, template_name):



    base = os.path.dirname(

        os.path.dirname(

            os.path.abspath(__file__)

        )

    )



    templates = {


    "Modern Resume":

    "modern_resume.docx",



    "ATS Resume":

    "ats_resume.docx",



    "Developer Resume":

    "developer_resume.docx"


    }



    template_path = os.path.join(

        base,

        "templates",

        templates[template_name]

    )



    if not os.path.exists(template_path):


        raise Exception(

            f"Template missing: {template_path}"

        )



    doc = Document(

        template_path

    )



    replacements = {


        "{{NAME}}":

        resume_data.get(

            "name",

            ""

        ),


        "{{SUMMARY}}":

        resume_data.get(

            "summary",

            ""

        ),


        "{{SKILLS}}":

        resume_data.get(

            "skills",

            ""

        ),



        "{{EXPERIENCE}}":

        resume_data.get(

            "experience",

            ""

        ),



        "{{PROJECTS}}":

        resume_data.get(

            "projects",

            ""

        ),



        "{{EDUCATION}}":

        resume_data.get(

            "education",

            ""

        )


    }



    replace_all(

        doc,

        replacements

    )



    output = "AI_Resume_Final.docx"



    doc.save(output)



    return output
