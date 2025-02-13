
import requests
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")
from langchain.embeddings import OpenAIEmbeddings

class ChatGPT():
    def __init__(self,api_key=None,model=None,config=None,db_launch=None):
        self.api_key = api_key
        self.model=model
        self.config=config
        self.db_launch=db_launch

    def get_embed_data(self,query):
        try:
            embeddings=OpenAIEmbeddings()
            query_vectors = embeddings.embed_query(query)

            sql_query = f"""select document , embedding <=> '{query_vectors}' as similarity
                            from {self.config['EMBEDIING_data']['database']}.{self.config['EMBEDIING_data']['table_name']}
                            ordey by similarity
                            limit 2"""
            
            data_df= self.db_launch.query_execute(q_type='select',query=sql_query)
            
            return  data_df['document'].to_string()

        except Exception as err:
            print("error while embedding query ",err)
            return "error while embedding query "+str(err)

    def chat_with_gpt(self,query):
        try:

            data = self.get_embed_data(query)

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
                "model":self.model,
                "messages": [
                        {"role": "system", "content": "Helpful HR policy assist"},
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
        

