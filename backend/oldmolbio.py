import sys
import os
import json
import time

from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import openai
import pinecone
from dotenv import load_dotenv

load_dotenv('.env')
""" openai_api_key = os.getenv('OPENAI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY') """
openai_api_key = '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'
pinecone_api_key = '5027b332-54e4-4a94-82da-42c3c2a44dc8'

with open('agents.json', 'r') as f:
    agentsData = json.load(f)

##this section connects to the pinecone index where we vectorized the OpenTrons API
openai.api_key = openai_api_key

pinecone.init(api_key=pinecone_api_key, enviroment="us-west1-gcp")


# connect to index
index_name = 'opentronsapi-docs'
index = pinecone.Index(index_name)

### a function to wait 4 seconds and retry up to 5 times in case there's an error, this guards against ratelimit errors
def retry_on_error(func, arg, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            result = func(arg)
            return result
        except Exception as e:
            if attempt < max_attempts - 1:  # no need to sleep on the last attempt
                print(f"Attempt {attempt + 1} failed. Retrying in 4 seconds.")
                time.sleep(4)
            else:
                print(f"Attempt {attempt + 1} failed. No more attempts left.")
                API_error = "OpenTronsAPI Error"
                return API_error


### this is a function that will take queries and return answers which draw upon the OpenTrons API index we built

def askOpenTrons(query):
    
  embed_model = agentsData[0]['embed_model']

  res = openai.Embedding.create(
      input=["Provide the exact code to perform this step:", query],
      engine=embed_model
  )

  # retrieve from Pinecone
  xq = res['data'][0]['embedding']

  # get relevant contexts (including the questions)
  res = index.query(xq, top_k=5, include_metadata=True)

  # get list of retrieved text
  contexts = [item['metadata']['text'] for item in res['matches']]

  augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query

  
  # system message to 'prime' the model
  template = (agentsData[5]['agent5_template'])

  res = openai.ChatCompletion.create(
      model=agentsData[0]['chat_model'],
      messages=[
          {"role": "system", "content": template},
          {"role": "user", "content": augmented_query}
      ]
  )

  return (res['choices'][0]['message']['content'])

#Layer 1
chat_1 = ChatOpenAI(streaming=False, callbacks=[StreamingStdOutCallbackHandler()], temperature=0, openai_api_key=openai_api_key)
template_1=agentsData[1]['agent1_template']
system_message_prompt_1 = SystemMessagePromptTemplate.from_template(template_1)
example_human = HumanMessagePromptTemplate.from_template(agentsData[1]['agent1_example1_human'])
example_ai = AIMessagePromptTemplate.from_template(agentsData[1]['agent1_example1_AI'])
human_template_1="{text}"
human_message_prompt_1 = HumanMessagePromptTemplate.from_template(human_template_1)
chat_prompt_1 = ChatPromptTemplate.from_messages([system_message_prompt_1, example_human, example_ai, human_message_prompt_1])
chain_1 = LLMChain(llm=chat_1, prompt=chat_prompt_1)




 #Layer 2
chat_2 = ChatOpenAI(streaming=False, callbacks=[StreamingStdOutCallbackHandler()], temperature=0, openai_api_key=openai_api_key)
template_2=agentsData[2]['agent2_template']
system_message_prompt_2 = SystemMessagePromptTemplate.from_template(template_2)
example_human = HumanMessagePromptTemplate.from_template(agentsData[2]['agent2_example1_human'])
example_ai = AIMessagePromptTemplate.from_template(agentsData[2]['agent2_example1_AI'])
human_template_2="{text}"
human_message_prompt_2 = HumanMessagePromptTemplate.from_template(human_template_2)
chat_prompt_2 = ChatPromptTemplate.from_messages([system_message_prompt_2, example_human, example_ai, human_message_prompt_2])
chain_2 = LLMChain(llm=chat_2, prompt=chat_prompt_2)



#Layer 3
chat_3 = ChatOpenAI(streaming=False, callbacks=[StreamingStdOutCallbackHandler()], temperature=0, openai_api_key=openai_api_key)
template_3=agentsData[3]['agent3_template']
system_message_prompt_3 = SystemMessagePromptTemplate.from_template(template_3)
example_human = HumanMessagePromptTemplate.from_template(agentsData[3]['agent3_example1_human'])
example_ai = AIMessagePromptTemplate.from_template(agentsData[3]['agent3_example1_AI'])
human_template_3="{text}"
human_message_prompt_3 = HumanMessagePromptTemplate.from_template(human_template_3)
chat_prompt_3 = ChatPromptTemplate.from_messages([system_message_prompt_3, example_human, example_ai, human_message_prompt_3])
chain_3 = LLMChain(llm=chat_3, prompt=chat_prompt_3)


#Layer 4

chat_4 = ChatOpenAI(streaming=False, callbacks=[StreamingStdOutCallbackHandler()], temperature=0, openai_api_key=openai_api_key)
template_4=agentsData[4]['agent4_template']
system_message_prompt_4 = SystemMessagePromptTemplate.from_template(template_4)
example_human = HumanMessagePromptTemplate.from_template(agentsData[4]['agent4_example1_human'])
example_ai = AIMessagePromptTemplate.from_template(agentsData[4]['agent4_example1_AI'])
human_template_4="{text}"
human_message_prompt_4 = HumanMessagePromptTemplate.from_template(human_template_4)
chat_prompt_4 = ChatPromptTemplate.from_messages([system_message_prompt_4, example_human, example_ai, human_message_prompt_4])
chain_4 = LLMChain(llm=chat_4, prompt=chat_prompt_4)

def main(user_input):
    output_string = ""

    output_1 = chain_1.run(user_input)
    raw_phases = output_1.split('|||')
    phases = [s for s in raw_phases if len(s) >= 10]
    output_string += "Here are all the phases at once\n\n"
    output_string += "\n".join(phases)
    output_string += "\n"

    for i, phase in enumerate(phases, 1):
        output_string += "\n\nPhase {}\n{}\n".format(i, phase)
        output_2 = chain_2.run(phase)

        raw_steps = output_2.split('|||')
        steps = [s for s in raw_steps if len(s) >= 10]
        output_string += "Here are all the steps at once for this phase\n\n"
        output_string += "\n".join(steps)
        output_string += "\n"

        for j, step in enumerate(steps, 1):
            output_string += "Step {}\n{}\n".format(j, step)
            output_3 = chain_3.run(step)

            raw_substeps = output_3.split('|||')
            substeps = [s for s in raw_substeps if len(s) >= 10]
            output_string += "Here are all the substeps at once for this step\n\n"
            output_string += "\n".join(substeps)
            output_string += "\n"

            for k, substep in enumerate(substeps, 1):
                output_string += "Substep {}\n{}\n".format(k, substep)
                output_4 = chain_4.run(substep)

                raw_commands = output_4.split('|||')
                commands = [s for s in raw_commands if len(s) >= 5]
                output_string += "Here are all the commands at once for this substep\n"
                output_string += "\n".join(commands)
                output_string += "\n"

                for l, command in enumerate(commands, 1):
                    output_string += "Line {}\n{}\n".format(l, command)
                    output_string += "Here is the code for this command\n"
                    output_string += retry_on_error(askOpenTrons,command)
                    output_string += "\n\n"

    return output_string

def test(user_input):
    time.sleep(30)
    user_input += "Successfully accessed\n"
    user_input += "molbio"
    return user_input

if __name__ == "__main__":
   ansewr = main("Make glow in the dark e. coli")
   with open('readme.txt', 'w') as f:
    f.write(answer)