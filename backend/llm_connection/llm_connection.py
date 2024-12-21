from openai import OpenAI
from secret import api_key
 

class LLMConnection():
    def __init__(self):
        base_url = "https://chat-ai.academiccloud.de/v1"
        
        self.model = "meta-llama-3.1-8b-instruct"
        self.client = OpenAI(
            api_key = api_key,
            base_url = base_url
        )

        self.chat_setup = {"role":"system","content":"You are a helpful assistant"}

    def text_completion(self,text):
        text_completion = self.client.completions.create(
            prompt=text,
            model= self.model,
        )

        return text_completion.choices[0].text
        

    def chat_completion(self,chat,question):
        if chat is None:
            chat = self.chat_setup

        chat_completion = self.client.chat.completions.create(
            messages=[chat,question],
            model= self.model,
        )

        return chat_completion.choices[0].message.content
    
def main():
    #print(LLMConnection().chat_completion(chat=None,question={"role":"user","content":"How tall is the Eiffel tower?"}))
    return

if __name__ == '__main__':
    main()