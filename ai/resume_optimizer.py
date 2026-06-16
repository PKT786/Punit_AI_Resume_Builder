from ai.openai_client import get_openai_client



def optimize_resume(resume_data):


    try:


        client = get_openai_client()



        prompt = f"""

You are an ATS resume expert.


Improve the following resume information.


Make it:

- ATS friendly

- Professional

- Recruiter friendly

- Achievement focused



Resume Data:


{resume_data}



Return only improved resume content.

"""



        response = client.chat.completions.create(


            model="gpt-4.1-mini",


            messages=[


                {

                    "role":"system",

                    "content":

                    "You are an expert ATS resume writer."

                },


                {

                    "role":"user",

                    "content":prompt

                }


            ],


            temperature=0.3


        )



        improved = response.choices[0].message.content



        return improved



    except Exception as e:


        print(

            "OpenAI Error:",

            e

        )


        # IMPORTANT
        # If AI unavailable,
        # return original data


        return resume_data