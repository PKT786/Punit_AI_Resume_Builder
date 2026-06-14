import subprocess



def convert_docx_to_pdf(docx_file):


    output_folder = "."


    subprocess.call(

        [

        "libreoffice",

        "--headless",

        "--convert-to",

        "pdf",

        docx_file,

        "--outdir",

        output_folder

        ]

    )


    pdf_file = docx_file.replace(

        ".docx",

        ".pdf"

    )


    return pdf_file
