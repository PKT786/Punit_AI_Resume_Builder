from docx import Document
import os
import tempfile



# -------------------------------------------------
# Replace text inside paragraph
# Handles Word split placeholders
# -------------------------------------------------

def replace_text_in_paragraph(paragraph, replacements):


    full_text = ""


    for run in paragraph.runs:

        full_text += run.text



    updated_text = full_text



    for key,value in replacements.items():


        if value is None:

            value = ""


        updated_text = updated_text.replace(

            key,

            str(value)

        )



    if updated_text != full_text:


        # clear existing runs

        for run in paragraph.runs:

            run.text = ""



        if paragraph.runs:


            paragraph.runs[0].text = updated_text



# -------------------------------------------------
# Replace inside tables
# -------------------------------------------------

def replace_text_in_table(table,replacements):


    for row in table.rows:


        for cell in row.cells:


            for paragraph in cell.paragraphs:


                replace_text_in_paragraph(

                    paragraph,

                    replacements

                )



# -------------------------------------------------
# Convert resume JSON into template placeholders
# -------------------------------------------------

def create_placeholder_mapping(data):


    mapping = {}



    # Simple fields

    simple_fields = [

        "name",

        "email",

        "phone",

        "location",

        "job_title",

        "summary"

    ]



    for field in simple_fields:


        mapping[

            "{{" + field.upper() + "}}"

        ] = data.get(

            field,

            ""

        )



    # Skills


    skills = data.get(

        "skills",

        []

    )


    if isinstance(skills,list):


        mapping["{{SKILLS}}"] = ", ".join(skills)


    else:


        mapping["{{SKILLS}}"] = skills



    # -------------------------------------------------
    # Education
    # -------------------------------------------------


    education = data.get(

        "education",

        []

    )


    for index,item in enumerate(

        education,

        1

    ):



        mapping[

        f"{{{{EDUCATION.{index}.DEGREE}}}}"

        ] = item.get(

            "degree",

            ""

        )



        mapping[

        f"{{{{EDUCATION.{index}.UNIVERSITY}}}}"

        ] = item.get(

            "university",

            ""

        )



        mapping[

        f"{{{{EDUCATION.{index}.YEAR}}}}"

        ] = item.get(

            "year",

            ""

        )



    # -------------------------------------------------
    # Experience
    # -------------------------------------------------


    experience = data.get(

        "experience",

        []

    )



    for index,item in enumerate(

        experience,

        1

    ):



        fields=[

            "role",

            "company",

            "location",

            "dates",

            "bullet1",

            "bullet2",

            "bullet3"

        ]



        for field in fields:


            mapping[

            f"{{{{EXPERIENCE.{index}.{field.upper()}}}}}"

            ] = item.get(

                field,

                ""

            )



    # -------------------------------------------------
    # Achievements
    # -------------------------------------------------


    achievements = data.get(

        "achievements",

        []

    )



    if isinstance(

        achievements,

        list

    ):


        mapping["{{ACHIEVEMENTS}}"] = "\n".join(

            achievements

        )


    else:


        mapping["{{ACHIEVEMENTS}}"] = achievements



    # -------------------------------------------------
    # Certifications
    # -------------------------------------------------


    certifications = data.get(

        "certifications",

        []

    )



    if isinstance(

        certifications,

        list

    ):


        mapping["{{CERTIFICATIONS}}"] = "\n".join(

            certifications

        )


    else:


        mapping["{{CERTIFICATIONS}}"] = certifications




    # -------------------------------------------------
    # Projects
    # -------------------------------------------------


    projects=data.get(

        "projects",

        []

    )



    for index,item in enumerate(

        projects,

        1

    ):



        mapping[

        f"{{{{PROJECTS.{index}.NAME}}}}"

        ] = item.get(

            "name",

            ""

        )



        mapping[

        f"{{{{PROJECTS.{index}.LINK}}}}"

        ] = item.get(

            "link",

            ""

        )



        mapping[

        f"{{{{PROJECTS.{index}.DESCRIPTION}}}}"

        ] = item.get(

            "description",

            ""

        )



    return mapping




# -------------------------------------------------
# Main DOCX Generator
# -------------------------------------------------

def create_docx(template_name,resume_data):


    template_path = os.path.join(

        "templates",

        template_name

    )



    if not os.path.exists(template_path):


        raise FileNotFoundError(

            f"Template not found: {template_path}"

        )



    doc = Document(

        template_path

    )



    replacements = create_placeholder_mapping(

        resume_data

    )



    # Paragraphs


    for paragraph in doc.paragraphs:


        replace_text_in_paragraph(

            paragraph,

            replacements

        )



    # Tables


    for table in doc.tables:


        replace_text_in_table(

            table,

            replacements

        )



    # Save generated file


    output_file = tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".docx"

    )



    doc.save(

        output_file.name

    )



    return output_file.name
