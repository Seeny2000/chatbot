# import os 
# import openai
# from dotenv import load_dotenv

# # openai_helper.api_key = ""
# load_dotenv()
# openai.api_key = "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"
# # openai_helper.api_key = os.getenv("OPENAI_API_KEY")

# def get_response(query):   
#     response = openai.ChatCompletion.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "you are a helpful to explain about this game website and gamming details."},
#             {"role": "user", "content": query}
#         ] ,
#         temperature=1.0 # temperature is 0 means its gives static ans thats why i give 2 
#     )

#     return response.choices[0].message["content"]

# from openai import OpenAI
# import os

# # Initialize the OpenAI client
# openai.api_key = "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"  # Replace with your actual API key

# def get_response(query):
#     response = openai.Chat.Completions.create(
#         model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant to explain about game websites and gaming details."},
#             {"role": "user", "content": query}
#         ],
#         temperature=1.0
#     )
#     return response.choices[0].message.content

import os
import openai

openai.api_key = "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"

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(query):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you are a helpful sales and marketing assistance."},
            {"role": "user", "content": query}
        ] ,
        temperature=2
    )

    return completion.choices[0].message["content"]