from docx import Document
import os
import re
import tempfile



def replace_text_in_paragraph(paragraph, replacements):


    full_text = ""


    for run in paragraph.runs:

        full_text += run.text



    updated_text = full_text



    for key,value in replacements.items():


        updated_text = updated_text.replace(

            key,

            str(value)

        )



    if updated_text != full_text:


        for run in paragraph.runs:

            run.text = ""


        if paragraph.runs:

            paragraph.runs[0].text = updated_text




def replace_in_table(table, replacements):


    for row in table.rows:


        for cell in row.cells:


            for paragraph in cell.paragraphs:


                replace_text_in_paragraph(

                    paragraph,

                    replacements

                )



def flatten_resume_data(data):


    result={}



    for key,value in data.items():


        if isinstance(value,list):


            for index,item in enumerate(value,1):


                if isinstance(item,dict):


                    for k,v in item.items():


                        result[

                        f"{{{{{key.upper()}.{index}.{k.upper()}}}}}"

                        ] = v



                else:


                    result[

                    f"{{{{{key.upper()}.{index}}}}}"

                    ] = item



        else:


            result[

            f"{{{{{key.upper()}}}}}"

            ] = value



    return result




def create_docx(template_name,resume_data):



    template_path = os.path.join(

        "templates",

        template_name

    )



    if not os.path.exists(template_path):


        raise FileNotFoundError(

            template_path

        )



    doc = Document(

        template_path

    )



    replacements = flatten_resume_data(

        resume_data

    )



    # Paragraph replacement

    for paragraph in doc.paragraphs:


        replace_text_in_paragraph(

            paragraph,

            replacements

        )



    # Table replacement

    for table in doc.tables:


        replace_in_table(

            table,

            replacements

        )



    output = tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".docx"

    )



    doc.save(

        output.name

    )



    return output.name
