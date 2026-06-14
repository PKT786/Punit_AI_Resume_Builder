from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter



def convert_docx_to_pdf(
    docx_file,
    resume_text
):

    """
    Creates PDF version of generated resume.

    DOCX template is used for Word.
    PDF is generated from resume content.
    """



    pdf_file = "AI_Resume.pdf"



    pdf = SimpleDocTemplate(

        pdf_file,

        pagesize=letter

    )



    styles = getSampleStyleSheet()



    content = []



    for line in resume_text.split("\n"):


        if line.strip():


            content.append(

                Paragraph(

                    line,

                    styles["Normal"]

                )

            )


            content.append(

                Spacer(

                    1,

                    10

                )

            )



    pdf.build(

        content

    )



    return pdf_file
