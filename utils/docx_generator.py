from docx import Document
import tempfile
import os
import re





def replace_in_paragraph(paragraph, mapping):


    text = paragraph.text



    for key,value in mapping.items():


        if value is None:

            value=""



        text=text.replace(

            key,

            str(value)

        )



    # remove remaining placeholders

    text=re.sub(

        r"\{\{.*?\}\}",

        "",

        text

    )



    if paragraph.runs:


        paragraph.runs[0].text=text



        for run in paragraph.runs[1:]:

            run.text=""





def replace_in_tables(doc,mapping):


    for table in doc.tables:


        for row in table.rows:


            for cell in row.cells:


                for paragraph in cell.paragraphs:


                    replace_in_paragraph(

                        paragraph,

                        mapping

                    )






def build_mapping(data):


    mapping={}



    basic_fields=[

        "name",

        "email",

        "phone",

        "location",

        "linkedin",

        "github",

        "job_title",

        "summary"

    ]



    for field in basic_fields:


        mapping[

            "{{"+field.upper()+"}}"

        ] = data.get(

            field,

            ""

        )




    mapping["{{SKILLS}}"] = ", ".join(

        data.get(

            "skills",

            []

        )

    )





    # Experience mapping


    experiences=data.get(

        "experience",

        []

    )



    for index in range(1,6):


        exp={}



        if index <= len(experiences):


            exp=experiences[index-1]




        mapping[

            f"{{{{EXPERIENCE.{index}.ROLE}}}}"

        ] = exp.get(

            "role",

            ""

        )



        mapping[

            f"{{{{EXPERIENCE.{index}.COMPANY}}}}"

        ] = exp.get(

            "company",

            ""

        )



        mapping[

            f"{{{{EXPERIENCE.{index}.DURATION}}}}"

        ] = exp.get(

            "duration",

            ""

        )



        mapping[

            f"{{{{EXPERIENCE.{index}.RESPONSIBILITIES}}}}"

        ] = "\n".join(

            exp.get(

                "responsibilities",

                []

            )

        )





    # Education


    education=data.get(

        "education",

        []

    )



    edu={}


    if education:

        edu=education[0]



    mapping["{{EDUCATION.DEGREE}}"] = edu.get(

        "degree",

        ""

    )



    mapping["{{EDUCATION.UNIVERSITY}}"] = edu.get(

        "university",

        ""

    )



    mapping["{{EDUCATION.YEAR}}"] = edu.get(

        "year",

        ""

    )





    # Projects


    projects=data.get(

        "projects",

        []

    )



    for index in range(1,6):


        project={}


        if index <= len(projects):

            project=projects[index-1]



        mapping[

            f"{{{{PROJECT.{index}.NAME}}}}"

        ] = project.get(

            "name",

            ""

        )


        mapping[

            f"{{{{PROJECT.{index}.DESCRIPTION}}}}"

        ] = project.get(

            "description",

            ""

        )



        mapping[

            f"{{{{PROJECT.{index}.LINK}}}}"

        ] = project.get(

            "link",

            ""

        )





    mapping["{{CERTIFICATIONS}}"] = "\n".join(

        data.get(

            "certifications",

            []

        )

    )



    mapping["{{ACHIEVEMENTS}}"] = "\n".join(

        data.get(

            "achievements",

            []

        )

    )



    return mapping







def create_docx(template_name,data):


    template_path=os.path.join(

        "templates",

        template_name

    )



    if not os.path.exists(template_path):


        raise FileNotFoundError(

            f"Template not found: {template_path}"

        )



    doc=Document(

        template_path

    )



    mapping=build_mapping(

        data

    )




    for paragraph in doc.paragraphs:


        replace_in_paragraph(

            paragraph,

            mapping

        )





    replace_in_tables(

        doc,

        mapping

    )





    output=tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".docx"

    )



    doc.save(

        output.name

    )



    return output.name
