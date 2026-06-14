from docx import Document



def create_docx(resume_data, template_name):


    templates = {


    "Modern Resume":
    "templates/modern_resume.docx",


    "ATS Resume":
    "templates/ats_resume.docx",


    "Developer Resume":
    "templates/developer_resume.docx"


    }



    doc = Document(

        templates[template_name]

    )



    replace = {


    "{{NAME}}":
    resume_data["name"],


    "{{SUMMARY}}":
    resume_data["summary"],


    "{{SKILLS}}":
    resume_data["skills"],


    "{{EXPERIENCE}}":
    resume_data["experience"],


    "{{PROJECTS}}":
    resume_data["projects"],


    "{{EDUCATION}}":
    resume_data["education"]


    }



    for p in doc.paragraphs:


        for key,value in replace.items():


            if key in p.text:


                p.text = p.text.replace(

                    key,

                    value

                )



    output="AI_Resume.docx"



    doc.save(output)



    return output
