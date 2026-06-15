from docx import Document
import os



# -------------------------------------------------
# Replace text inside paragraph runs
# -------------------------------------------------

def replace_in_paragraph(paragraph, replacements):


    for run in paragraph.runs:


        for key, value in replacements.items():


            if key in run.text:


                run.text = run.text.replace(

                    key,

                    str(value)

                )



# -------------------------------------------------
# Replace text inside tables
# -------------------------------------------------

def replace_in_table(table, replacements):


    for row in table.rows:


        for cell in row.cells:


            for paragraph in cell.paragraphs:


                replace_in_paragraph(

                    paragraph,

                    replacements

                )



# -------------------------------------------------
# Replace headers and footers
# -------------------------------------------------

def replace_headers_footers(doc, replacements):


    for section in doc.sections:


        # Header

        for paragraph in section.header.paragraphs:


            replace_in_paragraph(

                paragraph,

                replacements

            )



        # Footer

        for paragraph in section.footer.paragraphs:


            replace_in_paragraph(

                paragraph,

                replacements

            )



# -------------------------------------------------
# Main replacement function
# -------------------------------------------------

def replace_placeholders(doc, replacements):


    # Normal paragraphs


    for paragraph in doc.paragraphs:


        replace_in_paragraph(

            paragraph,

            replacements

        )



    # Tables


    for table in doc.tables:


        replace_in_table(

            table,

            replacements

        )



    # Header Footer


    replace_headers_footers(

        doc,

        replacements

    )



# -------------------------------------------------
# Create Resume DOCX
# -------------------------------------------------

def create_docx(template_name, resume_data):


    template_path = os.path.join(

        "templates",

        template_name

    )



    if not os.path.exists(template_path):


        raise FileNotFoundError(

            f"Template not found: {template_path}"

        )



    # Open template


    doc = Document(

        template_path

    )



    # Data mapping


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



        "{{LOCATION}}":

        resume_data.get(

            "location",

            ""

        ),



        "{{LINKEDIN}}":

        resume_data.get(

            "linkedin",

            ""

        ),



        "{{GITHUB}}":

        resume_data.get(

            "github",

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



    # Replace values


    replace_placeholders(

        doc,

        replacements

    )



    # Output file


    output_file = "Generated_Resume.docx"



    doc.save(

        output_file

    )



    return output_file
