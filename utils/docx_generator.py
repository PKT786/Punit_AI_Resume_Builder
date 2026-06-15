from docx import Document

import os



def replace_text(document, replacements):


    # Paragraphs


    for paragraph in document.paragraphs:


        for key,value in replacements.items():


            if key in paragraph.text:


                paragraph.text = paragraph.text.replace(

                    key,

                    value

                )



    # Tables


    for table in document.tables:


        for row in table.rows:


            for cell in row.cells:


                for paragraph in cell.paragraphs:


                    for key,value in replacements.items():


                        if key in paragraph.text:


                            paragraph.text = paragraph.text.replace(

                                key,

                                value

                            )





def create_docx(template_name, resume_data):


    base = os.getcwd()



    template_path = os.path.join(

        base,

        "templates",

        template_name

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



        "{{JOB_TITLE}}":

        resume_data.get(

            "job_title",

            ""

        ),



        "{{EMAIL}}":

        resume_data.get(

            "email",

            ""

        ),



        "{{PHONE}}":

        resume_data.get(

            "phone",

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



        "{{EDUCATION}}":

        resume_data.get(

            "education",

            ""

        )



    }



    replace_text(

        doc,

        replacements

    )



    output = "Generated_Resume.docx"



    doc.save(output)



    return output