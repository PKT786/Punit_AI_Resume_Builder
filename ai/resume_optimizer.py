from ai.openai_client import get_openai_client



def optimize_resume(resume_text):


    client = get_openai_client()



    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[


            {

            "role":"system",

            "content":

            """
            You are an expert ATS resume writer.

            Improve resume:

            - Add professional wording
            - Add ATS keywords
            - Convert responsibilities into achievements
            - Keep information truthful

            """

            },


            {

            "role":"user",

            "content":resume_text

            }


        ]

    )


    return response.choices[0].message.content