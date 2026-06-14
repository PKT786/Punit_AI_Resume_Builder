from docx import Document
import os



def create_docx(
    resume_data,
    template_name
):


    template_map = {


    "Modern Resume":
    "templates/modern_resume.docx",


    "ATS Resume":
    "templates/ats_resume.docx",


    "Developer Resume":
    "templates/developer_resume.docx"


    }



    template_file = template_map[
        template_name
    ]



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




    for paragraph in doc.paragraphs:


        for key,value in replacements.items():


            if key in paragraph.text:


                paragraph.text = paragraph.text.replace(

                    key,

                    value

                )



    output = "Generated_AI_Resume.docx"



    doc.save(output)



    return output
