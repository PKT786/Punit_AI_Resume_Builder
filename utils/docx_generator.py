from docx import Document
import tempfile
import os





def replace_all(doc,mapping):


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


    template=os.path.join(

        "templates",

        template_name

    )


    doc=Document(template)





    mapping={


    "{{NAME}}":data.get("name",""),

    "{{JOB_TITLE}}":data.get("job_title",""),

    "{{EMAIL}}":data.get("email",""),

    "{{PHONE}}":data.get("phone",""),

    "{{LOCATION}}":data.get("location",""),

    "{{LINKEDIN}}":data.get("linkedin",""),

    "{{GITHUB}}":data.get("github",""),

    "{{SUMMARY}}":data.get("summary",""),

    "{{SKILLS}}":data.get("skills","")

    }




    exp=data["experience"][0]



    mapping.update({

    "{{EXPERIENCE.1.ROLE}}":exp.get("role",""),

    "{{EXPERIENCE.1.COMPANY}}":exp.get("company",""),

    "{{EXPERIENCE.1.DATES}}":exp.get("dates",""),

    "{{EXPERIENCE.1.LOCATION}}":exp.get("location",""),

    "{{EXPERIENCE.1.BULLET1}}":exp.get("bullet1",""),

    "{{EXPERIENCE.1.BULLET2}}":exp.get("bullet2",""),

    "{{EXPERIENCE.1.BULLET3}}":exp.get("bullet3","")

    })




    project=data["projects"][0]



    mapping.update({

    "{{PROJECTS.1.NAME}}":project.get("name",""),

    "{{PROJECTS.1.DESCRIPTION}}":project.get("description",""),

    "{{PROJECTS.1.LINK}}":project.get("link","")

    })




    replace_all(

        doc,

        mapping

    )




    output=tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".docx"

    )



    doc.save(output.name)



    return output.name
