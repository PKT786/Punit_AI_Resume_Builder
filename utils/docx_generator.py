from docx import Document
import tempfile
import os



def replace_text(doc, mapping):


    for p in doc.paragraphs:


        for key,value in mapping.items():

            if key in p.text:


                p.text=p.text.replace(

                    key,

                    value

                )



    for table in doc.tables:


        for row in table.rows:


            for cell in row.cells:


                for p in cell.paragraphs:


                    for key,value in mapping.items():


                        if key in p.text:


                            p.text=p.text.replace(

                                key,

                                value

                            )






def create_docx(template_name,data):


    path=os.path.join(

        "templates",

        template_name

    )


    doc=Document(path)



    mapping={


    "{{NAME}}":data.get("name",""),

    "{{EMAIL}}":data.get("email",""),

    "{{PHONE}}":data.get("phone",""),

    "{{LOCATION}}":data.get("location",""),

    "{{JOB_TITLE}}":data.get("job_title",""),

    "{{SUMMARY}}":data.get("summary",""),

    "{{SKILLS}}":

    ", ".join(data.get("skills",[]))


    }




    exp=data.get("experience",[])



    for i,e in enumerate(exp,start=1):


        mapping[f"{{{{EXPERIENCE.{i}.ROLE}}}}"]=e.get(
            "role",
            ""
        )


        mapping[f"{{{{EXPERIENCE.{i}.COMPANY}}}}"]=e.get(
            "company",
            ""
        )


        mapping[f"{{{{EXPERIENCE.{i}.DURATION}}}}"]=e.get(
            "duration",
            ""
        )


        mapping[f"{{{{EXPERIENCE.{i}.RESPONSIBILITIES}}}}"]=

        "\n".join(

            e.get(
                "responsibilities",
                []
            )

        )





    replace_text(

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
