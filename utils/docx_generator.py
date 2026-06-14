from docx import Document
import os



def replace_text(doc, replacements):


    for paragraph in doc.paragraphs:


        for key,value in replacements.items():


            if key in paragraph.text:


                paragraph.text = paragraph.text.replace(

                    key,

                    value

                )



    for table in doc.tables:


        for row in table.rows:


            for cell in row.cells:


                for paragraph in cell.paragraphs:


                    for key,value in replacements.items():


                        if key in paragraph.text:


                            paragraph.text = paragraph.text.replace(

                                key,

                                value

                            )




def create_docx(resume_data, template_name):



    base_path = os.path.dirname(

        os.path.dirname(

            os.path.abspath(__file__)

        )

    )



    template_folder = os.path.join(

        base_path,

        "templates"

    )



    templates = {


    "Modern Resume":

    os.path.join(

        template_folder,

        "modern_resume.docx"

    ),



    "ATS Resume":

    os.path.join(

        template_folder,

        "ats_resume.docx"

    ),



    "Developer Resume":

    os.path.join(

        template_folder,

        "developer_resume.docx"

    )


    }



    template_file = templates.get(

        template_name

    )



    if not template_file or not os.path.exists(template_file):


        raise FileNotFoundError(

        f"""

Template missing:

{template_file}


Please upload DOCX files inside templates folder.

"""

        )




    doc = Document(

        template_file

    )



    replacements = {


    "{{NAME}}":

    resume_data.get("name",""),


    "{{SUMMARY}}":

    resume_data.get("summary",""),


    "{{SKILLS}}":

    resume_data.get("skills",""),


    "{{EXPERIENCE}}":

    resume_data.get("experience",""),


    "{{PROJECTS}}":

    resume_data.get("projects",""),


    "{{EDUCATION}}":

    resume_data.get("education","")


    }



    replace_text(

        doc,

        replacements

    )



    output = "AI_Resume.docx"



    doc.save(output)



    return output
