from langchain import FewShotPromptTemplate
import os
import datetime
from langchain import LLMChain, OpenAI, SQLDatabase, SQLDatabaseChain

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def format_events_query(query):
    examples = [
        {
            "Query": "What events are happening this weekend?",
            "Answer": """
            Event Name: Music Festival XYZ
            Description: Join us for a weekend filled with live music performances from various artists.
            Start Time: Saturday, July 17th, 2023, 6:00 PM
            End Time: Sunday, July 18th, 2023, 11:00 PM
            Location: City Park
            Number of Upvotes: 50
            Sharable Link: https://musicfestivalxyz.com"""
        },
        {
            "Query": "Are there any art exhibitions this month?",
            "Answer": """
            Event Name: Art Exhibition ABC
            Description: Explore a diverse collection of artworks from local and international artists.
            Start Time: Friday, July 23rd, 2023, 10:00 AM
            End Time: Sunday, July 25th, 2023, 6:00 PM
            Location: Art Gallery XYZ
            Number of Upvotes: 30
            Sharable Link: https://artexhibitionabc.com"""
        },
        {
            "Query": "Tell me about the upcoming conference on technology.",
            "Answer": """
            Event Name: Tech Conference 2023
            Description: Join industry experts for insightful sessions on the latest advancements in technology.
            Start Time: Wednesday, August 2nd, 2023, 9:00 AM
            End Time: Thursday, August 3rd, 2023, 5:00 PM
            Location: Convention Center
            Number of Upvotes: 70
            Sharable Link: https://techconference2023.com"""
        },
        {
            "Query": "Is there a food festival happening next week?",
            "Answer": """
            Event Name: Food Fest ABC
            Description: Indulge in a culinary journey with a wide range of delicious dishes from around the world.
            Start Time: Friday, July 28th, 2023, 5:00 PM
            End Time: Sunday, July 30th, 2023, 10:00 PM
            Location: Downtown Square
            Number of Upvotes: 45
            Sharable Link: https://foodfestabc.com"""
        }
    ]

    example_template = """
    User: {query}
    AI: {answer}
    """

    example_prompt = PromptTemplate(
        input_variables=["query", "answer"],
        template=example_template
    )

    prefix = """The following are responses from conversations with an AI
    assistant. you are  known to be a very smart text formater it are great at formating  content about events  in a concise and easy to understand manner without changing anything or making a meaning out of it. \
    when given a bunch of data about evenst containing infomation of event name, description, start timme, end time loacation and sharable link and number of upvotes the event has.\
    you organise them a list structure like. \
    examples:
    """

    suffix = """
    User: {query}
    AI: """

    few_shot_prompt_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["query"],
        example_separator="\n\n"
    )

    chain = LLMChain(llm=chat, prompt=few_shot_prompt_template)
    return chain.run(query)
