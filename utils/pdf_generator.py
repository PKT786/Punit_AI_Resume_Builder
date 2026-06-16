import os
import subprocess
import platform



def convert_to_pdf(docx_file):


    if not os.path.exists(docx_file):

        raise FileNotFoundError(

            f"DOCX file not found: {docx_file}"

        )



    output_dir = os.path.dirname(

        docx_file

    )



    system = platform.system()



    # Streamlit Cloud Linux

    if system == "Linux":


        subprocess.run(

            [

                "libreoffice",

                "--headless",

                "--convert-to",

                "pdf",

                "--outdir",

                output_dir,

                docx_file

            ],

            check=True

        )



    else:


        # Windows / Local

        from docx2pdf import convert


        convert(

            docx_file,

            output_dir

        )



    pdf_file = docx_file.replace(

        ".docx",

        ".pdf"

    )



    if not os.path.exists(pdf_file):


        raise Exception(

            "PDF conversion failed"

        )



    return pdf_file
