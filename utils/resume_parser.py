import PyPDF2
from docx import Document



def extract_resume_text(file):


    text=""


    if file.name.endswith(".pdf"):


        reader = PyPDF2.PdfReader(file)


        for page in reader.pages:

            text += page.extract_text()



    elif file.name.endswith(".docx"):


        doc = Document(file)


        for para in doc.paragraphs:

            text += para.text + "\n"



    return text