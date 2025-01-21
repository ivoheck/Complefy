import os
import sys

# Verzeichnis des Projekts (Root-Verzeichnis) ermitteln
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))  # Passe die Anzahl der '..' an

# Projekt-Root zu sys.path hinzufügen, falls noch nicht enthalten
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from openai import OpenAI
from secret import api_key
import json
import ast
from backend.llm_connection import promts
import asyncio
import ast


class ChatObject():

    def __init__(self):
        self.chat = [{"role":"system","content":"You are a helpful assistant"}]

    def add_user_promt(self, chat, promt):
        chat.append({"role":"user","content": str(promt)})
        return chat
    
    def add_respones(self, chat, respose):
        chat.append({"role":"user","content": str(respose)})
        return chat
    
    def get_chat(self):
        return self.chat


class LLMConnection():
    def __init__(self):
        base_url = "https://chat-ai.academiccloud.de/v1"
        
        self.model = "meta-llama-3.1-8b-instruct"
        self.model_lama_70 = "meta-llama-3.1-70b-instruct"
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
        

    def chat_completion(self,chat,question,model):

        if model == None:
            model = self.model
        chat = None
        #print(question)
        if chat is None:
            chat = self.chat_setup

        chat_completion = self.client.chat.completions.create(
            messages=[chat,question],
            model= model,
        )

        return chat_completion.choices[0].message.content
    
    async def chat_completion_async(self,chat,question,model):

        chat = None
        #print(question)
        if chat is None:
            chat = self.chat_setup

        # chat_completion = await self.client.chat.completions.create(
        #     messages=[chat,question],
        #     model= model,
        # )
        chat_completion = await asyncio.to_thread(self.client.chat.completions.create,
                                              messages=[chat, question],
                                              model=model)

        return chat_completion.choices[0].message.content
    
    def get_result_awnser(self,message,results):
        chat = [{"role":"system","content":"You are a helpful assistant"}]

        promt = """
                generire eine kurze antwort nachricht für basirend auf der aufforderung des nutzers und der ergebnisse, soetws wie: hier sind die ergebnisse...
                nim auch kurz bezug auf die gefundenen ergebnisse
            """
        promt += "die ergebnisse sind follgende: " + str(results)
        promt += "die aufforderung des nutzer ist: " + message
        complete_promt = {"role":"user","content":promt}
        
        return self.chat_completion(chat=chat,question=complete_promt,model=self.model_lama_70)
        
    async def get_results_async(self,input_comps,input_promt):
        chat = [{"role":"system","content":"You are a helpful assistant"}]
                 
        promt =  promts.get_result
                 
        promt = promt + f"{input_comps} Der Kontext-Prompt lautet: {input_promt}"
        complete_promt = {"role":"user","content":promt}
        result =  await self.chat_completion_async(chat=chat,question=complete_promt,model=self.model_lama_70)
        start_index = result.find('[')  # Finde den Anfang der JSON-Daten
        end_index = result.rfind(']') + 1  # Finde das Ende der JSON-Daten

        json_string = result[start_index:end_index]
        #print(json_string)

        try:
            data_dict = ast.literal_eval(json_string)
            return (data_dict,None)
        except:
            return (None, json_string)
        

    def get_results(self,input_comps,input_promt):
        chat = [{"role":"system","content":"You are a helpful assistant"}]
                 
        promt =  promts.get_result
                 
        promt = promt + f"{input_comps} Der Kontext-Prompt lautet: {input_promt}"
        complete_promt = {"role":"user","content":promt}
        result =  self.chat_completion(chat=chat,question=complete_promt,model=self.model_lama_70)
        start_index = result.find('[')  # Finde den Anfang der JSON-Daten
        end_index = result.rfind(']') + 1  # Finde das Ende der JSON-Daten

        json_string = result[start_index:end_index]
        #print(json_string)

        try:
            data_dict = ast.literal_eval(json_string)
            return (data_dict,None)
        except:
            return (None, json_string)
        
    
def main():
    print(LLMConnection().chat_completion(chat=None,question={"role":"user","content":"How tall is the Eiffel tower?"},model=None))
    #print( '\n \n' , LLMConnection().get_results(input_comps=))
    

if __name__ == '__main__':
    main()