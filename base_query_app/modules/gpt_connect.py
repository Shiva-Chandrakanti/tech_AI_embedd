
import requests
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")

class ChatGPT():
    def __init__(self,api_key=None):
        self.api_key = api_key

    def chat_with_gpt(self,query,data,content):
        try:
            print("start calling gpt api - ",datetime.now())
            # Define the API endpoint
            api_endpoint = "https://api.openai.com/v1/chat/completions"

            # Define the headers for the HTTP request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            # Define the payload for the API request
            # query= "what is 1+1"
            print("gpt data")
            payload = {
                # "model": "gpt-3.5-turbo-0301",
                "model":"gpt-4-32k",
                "messages": [
                        {"role": "system", "content": "Helpful HR policy assist"},
                        {"role": "system", "content": "If user is just greeting instead of asking questions related to the data, please greet the user by addressing the name in return by saying you can assist the user in getting knowledge only about different HR policies of the company like leave policy, dress policy, code of conduct, shift allowance policy, exit policy"},
                        {"role": "user", "content": content},
                        {"role": "user", "content": "user mail id is : shivani.mandwal@factspan.com ,user name is : Shivani Mandwal" },
                        {"role": "user", "content": "Answer the following query using only the data:\n {} ".format(data)},
                        {"role": "user", "content": query}
                    ]
            }

            # Send the HTTP POST request to the API endpoint
            response = requests.post(api_endpoint, headers=headers, json=payload)

            # Parse the JSON response
            data = response.json()
            print(data)
            # Extract the generated message from the API response
            try:
                message = data["choices"][0]["message"]["content"]
            except:
                message = data['error']['message']
            print("end time to get response from gpt api - ",datetime.now())

            return message
        except Exception as err:
            print("Error while getting the response from chatGPT : ",err)
            return "Error while getting the response from chatGPT : "+str(err)
