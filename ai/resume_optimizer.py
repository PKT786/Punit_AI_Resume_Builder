from ai.openai_client import get_openai_client
import streamlit as st



# ---------------------------------
# Template Resume Generator
# ---------------------------------

def template_resume(resume_text, template):


    if template == "Modern Resume":


        return f"""

PROFESSIONAL RESUME


PROFESSIONAL SUMMARY


{resume_text}



KEY SKILLS


• Technical Skills

• Problem Solving

• Communication

• Team Collaboration



PROFESSIONAL EXPERIENCE


• Delivered business solutions

• Worked on technical requirements

• Improved process efficiency



PROJECTS


Project Name:

Description:

Technology Used:



EDUCATION


Add Education Details

"""



    elif template == "Developer Resume":


        return f"""


SOFTWARE DEVELOPER RESUME



SUMMARY


{resume_text}



TECHNICAL SKILLS


Programming:
Python | SQL | Java


Tools:
Git | Cloud | VS Code



EXPERIENCE


• Developed software solutions

• Fixed technical issues

• Improved application performance



PROJECTS


Project Name:

Technology Stack:

Description:



EDUCATION


Add Education Details

"""



    else:


        return f"""


ATS FRIENDLY RESUME



PROFESSIONAL SUMMARY


{resume_text}



CORE SKILLS


• Technical Skills

• Industry Knowledge

• Tools & Technologies



WORK EXPERIENCE


• Created business impact

• Improved workflows

• Delivered projects



PROJECTS


Project Name:

Description:



EDUCATION


Add Education Details

"""




# ---------------------------------
# AI Resume Optimizer
# ---------------------------------


def optimize_resume(
        resume_text,
        template="ATS Resume"
):


    try:


        client = get_openai_client()



        response = client.chat.completions.create(


            model="gpt-4.1-mini",


            messages=[


                {

                "role":"system",

                "content":

                f"""

You are a professional ATS resume writer.

Create a premium {template}.


Rules:

- Improve professional wording
- Add ATS keywords
- Convert tasks into achievements
- Use bullet points
- Do not create fake experience

Output only resume content.

No explanation.

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



        error=str(e)



        if "insufficient_quota" in error:


            st.warning(
            """
            ⚠️ AI Optimization unavailable.

            OpenAI API quota limit reached.

            Creating resume using selected template.
            """
            )



        else:


            st.warning(
            """
            ⚠️ AI service unavailable.

            Creating resume using selected template.
            """
            )



        # ONLY RETURN RESUME
        return template_resume(

            resume_text,

            template

        )
