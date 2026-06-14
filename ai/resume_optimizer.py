from ai.openai_client import get_openai_client



def template_resume(resume_text, template):

    """
    Fallback ATS resume generator
    Works even when OpenAI is unavailable
    """


    if template == "Modern Resume":


        return f"""

================================

PROFESSIONAL RESUME


SUMMARY

{resume_text}



SKILLS

• Technical Skills
• Problem Solving
• Communication
• Team Collaboration



EXPERIENCE

• Responsible for delivering quality solutions

• Worked on business requirements

• Improved process efficiency



PROJECTS

Project Name:

Description:

Technology Used:



EDUCATION

Add education details


================================

"""


    elif template == "Developer Resume":


        return f"""


SOFTWARE DEVELOPER RESUME


PROFESSIONAL SUMMARY


{resume_text}



TECHNICAL SKILLS


Programming:

Python | SQL | Java


Tools:

Git | VS Code | Cloud



PROJECT EXPERIENCE


• Developed applications

• Created solutions using technology

• Debugged and improved systems



GITHUB:

Portfolio:


"""


    else:


        return f"""


ATS FRIENDLY RESUME


PROFESSIONAL SUMMARY


{resume_text}



CORE SKILLS


• Add relevant keywords

• Add technical skills

• Add domain expertise



WORK EXPERIENCE


• Achievement based bullet points

• Add measurable results


PROJECTS


Project Name

Description


EDUCATION


"""


# ---------------------------------
# OpenAI Optimizer
# ---------------------------------


def optimize_resume(resume_text, template="ATS Resume"):


    try:


        client = get_openai_client()



        response = client.chat.completions.create(


            model="gpt-4.1-mini",


            messages=[


                {


                "role":"system",


                "content":

                f"""

You are an expert ATS resume writer.

Create a premium {template}.

Rules:

- Use professional language
- Add ATS keywords
- Improve experience bullets
- Add achievements
- Improve formatting
- Do not create fake experience

Make it recruiter ready.

"""

                },


                {


                "role":"user",


                "content":resume_text


                }


            ],


            temperature=0.3


        )



        return response.choices[0].message.content



    except Exception as e:



        error_message = str(e)



        # --------------------------
        # API quota error handling
        # --------------------------


        if "insufficient_quota" in error_message:


            return f"""

⚠️ AI Optimization temporarily unavailable.

Reason:
OpenAI API quota limit reached.

Generating ATS Resume using
{template} template.

----------------------------


{template_resume(
    resume_text,
    template
)}


"""


        else:


            return f"""

⚠️ AI service error.

Generating standard ATS resume.


{template_resume(
    resume_text,
    template
)}

"""
