from ai.openai_client import get_openai_client



def optimize_resume(resume_text):


    client = get_openai_client()


    try:


        response = client.chat.completions.create(


            model="gpt-4.1-mini",


            messages=[


                {
                    "role":"system",

                    "content":
                    """
                    You are an expert ATS resume writer.

                    Improve resume:
                    - Professional summary
                    - Skills
                    - Experience bullets
                    - ATS keywords

                    Do not create fake experience.
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


        return f"""
        OpenAI Error:

        {str(e)}
        """
