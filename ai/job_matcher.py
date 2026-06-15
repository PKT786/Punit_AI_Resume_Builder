from ai.openai_client import get_openai_client



def match_job(resume, job_description):


    client = get_openai_client()



    response = client.chat.completions.create(


        model="gpt-4.1-mini",


        messages=[


        {

        "role":"system",

        "content":
        """
        You are an ATS recruiter.
        Compare resume with job description.
        Provide match percentage and missing skills.
        """

        },


        {

        "role":"user",

        "content":f"""

        Resume:

        {resume}


        Job Description:

        {job_description}


        """

        }


        ]

    )


    return response.choices[0].message.content