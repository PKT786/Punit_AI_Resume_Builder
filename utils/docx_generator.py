from docx import Document



def create_docx(content):


    file_path = "AI_Resume.docx"



    doc = Document()



    doc.add_heading(
        "Professional Resume",
        level=1
    )



    for line in content.split("\n"):


        doc.add_paragraph(
            line
        )



    doc.save(file_path)



    return file_path