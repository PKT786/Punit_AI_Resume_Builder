from ai.openai_client import get_openai_client



def optimize_resume(resume_json):


    try:


        client = get_openai_client()



        response = client.chat.completions.create(


            model="gpt-4.1-mini",


            messages=[


                {


                "role":"system",

                "content":

                """

You are an expert ATS resume writer.

Improve resume content.

Make it:

- Professional

- ATS friendly

- Achievement focused

Return only improved resume content.

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



        return resume_text