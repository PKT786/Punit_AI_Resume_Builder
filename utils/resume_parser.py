from docx import Document


def extract_resume(file):


    doc = Document(file)


    text = ""


    for p in doc.paragraphs:

        text += p.text + "\n"



    return text