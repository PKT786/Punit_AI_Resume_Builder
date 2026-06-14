from docx import Document



def replace_text(doc, replacements):


    # paragraphs

    for paragraph in doc.paragraphs:


        for key,value in replacements.items():


            if key in paragraph.text:


                paragraph.text = paragraph.text.replace(

                    key,

                    value

                )



    # tables

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


    templates={


    "Modern Resume":
    "templates/modern_resume.docx",


    "ATS Resume":
    "templates/ats_resume.docx",


    "Developer Resume":
    "templates/developer_resume.docx"


    }



    doc=Document(

        templates[template_name]

    )



    replacements={


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



    output="AI_Resume.docx"



    doc.save(output)



    return output
