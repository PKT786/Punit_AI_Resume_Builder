from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet



def create_pdf(content):


    file_path = "AI_Resume.pdf"



    doc = SimpleDocTemplate(
        file_path
    )


    styles = getSampleStyleSheet()



    story=[]



    for line in content.split("\n"):


        story.append(

            Paragraph(
            line,
            styles["Normal"]
            )

        )


        story.append(
            Spacer(1,12)
        )



    doc.build(
        story
    )



    return file_path