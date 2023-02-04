import os
import openai
# load API key
from dotenv import load_dotenv

class OpenAI:
  def __init__(self):
    load_dotenv()
    self.openai = openai
    self.openai.organization = "org-5gENU5KakWtwak6ahoqwkYnS"
    self.openai.api_key = os.getenv("OPENAI_API_KEY")
    
  def getResponse(self, inputPrompt):
    response = self.openai.Completion.create(
      model="text-davinci-003",
      prompt= inputPrompt,
      temperature=0.5,
      max_tokens=150,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )
    
    return response["choices"][0]["text"]

# openaiOb = OpenAI()
# print(openaiOb.getResponse('what is love'))
