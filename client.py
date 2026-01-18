# from google import genai

# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents="Explain how AI works in a few words",
# )

# print(response.text)

# import google.generativeai as genai

# genai.configure(api_key="AIzaSyAxXoj8cYx_yYb0-AktHUpQs0cUlZedAmQ")

# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("What is coding?")
# print(response.text)

# from google import genai
# import os

# client = genai.Client(api_key=os.getenv("AIzaSyAxXoj8cYx_yYb0-AktHUpQs0cUlZedAmQ"))

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents="Explain how AI works in a few words",
# )

# print(response.text)

#! from google import genai

# client = genai.Client(api_key="AIzaSyAxXoj8cYx_yYb0-AktHUpQs0cUlZedAmQ")

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents=[
#         "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Cloud.",
#         "User asks: What is coding?"
#     ]
# )

#! print(response.text.content)



# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents= [
#         {"role": "system" , "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud"} ,
#         {"role": "user" , "content": "What is coding"}
#     ]
# )


from google import genai

client = genai.Client(api_key="AIzaSyAxXoj8cYx_yYb0-AktHUpQs0cUlZedAmQ")

def get_jarvis_reply(user_command: str) -> str:
    prompt = f"""
    You are Jarvis, a helpful virtual assistant.
    User said: {user_command}
    Respond briefly.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text   # <-- THIS is the export you want
