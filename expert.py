from dotenv import load_dotenv
from expertai.nlapi.cloud.client import ExpertAiClient
client = ExpertAiClient()
load_dotenv()



def expert_ai_analysis( text_input: str):
    """
    Function to call expert.ai cloud api. Pass in a str to return full analysis. If error returns None.
    """
    language = 'en'
    try: 
        output = client.full_analysis(body={"document": {"text": text_input}}, params={'language': language})

        entities = [e.lemma for e in output.entities]
        main_phrases =  [p.value for p in output.main_phrases]
        main_lemmas =  [l.value for l in output.main_lemmas]
        topics =  [t.label for t in output.topics]
        sentiment = output.sentiment.overall

    except Exception as error:
        print(error)
        return None
    return {'entities': entities, 'main_phrases': main_phrases, 'main_lemmas': main_lemmas, 'topics': topics, 'sentiment': sentiment}

