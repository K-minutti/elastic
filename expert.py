from dotenv import load_dotenv
from expertai.nlapi.cloud.client import ExpertAiClient
client = ExpertAiClient()
load_dotenv()

text = "Michael Jordan was one of the best basketball players of all time. Scoring was Jordan's stand-out skill, but he still holds a defensive NBA record, with eight steals in a half."
language= 'en'

# output = client.specific_resource_analysis(body={'document':{"text": text}}, params={'language': language, 'resource': 'entities'})

# print(f'{"ENTITY":{50}} {"TYPE":{10}}')
# print(f'{"------":{50}} {"----":{10}}')

# for entity in output.entities:
#     print(f'{entity.lemma:{50}} {entity.type_:{10}}')
output = client.full_analysis(body={"document": {"text": text}}, params={'language': language})


# Output arrays size

print("Output arrays size:")

print("knowledge: ", len(output.knowledge))
print("paragraphs: ", len(output.paragraphs))
print("sentences: ", len(output.sentences))
print("phrases: ", len(output.phrases))
print("tokens: ", len(output.tokens))
print("mainSentences: ", len(output.main_sentences))
print("mainPhrases: ", len(output.main_phrases))
print("mainLemmas: ", len(output.main_lemmas))
print("mainSyncons: ", len(output.main_syncons))
print("topics: ", len(output.topics))
print("entities: ", len(output.entities))
print("relations: ", len(output.relations))
print("sentiment.items: ", [item.items for item in output.sentiment.items], output.sentiment.overall)

"""
We need a function/class that takes a 
piece of text and params for the type of analysis we want to perform


at this point I will just use the sentiment.overall
main phrases and main Lemmas 
we can to entities 
and topics
now we need to figure out how to extract all of the items for each output we want 

I want main phrases as an a 1D array of type text -> [phrases]
I want the same as above for main Lemmas AND Topics and Entities 
Then for Sentiment it will just be stored as a or NUMERICA  (5,2) SHOULD BE 100.00 and -100.00 as min I believe 

entities -> can only be of type Person , Organization, Business/Companies, maybe a few others


What are going  to do if the expert ai cannot parse the text passed in?


"""