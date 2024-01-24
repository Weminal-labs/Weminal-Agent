



from Oraidex_models.config import Config
from Oraidex_models.tool import StockScreenerTool, search_price_orai
from secret import load_secrets

from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain import LLMChain


load_secrets()


# StockScreenerTool()

tools = [     
    StockScreenerTool(),
    Tool(
        name="search for Oraichain Ecosystem",
        func= SerpAPIWrapper().run,
        description="Use when you are asked to search internet  not about Oraidex tool or price orai. This will output rely on user requirement. You should answer directly to the question",
    ),
    Tool(
        func=search_price_orai,
        name="search price orai token",
        description="Use only when you need to get orai token ticker from internet. Only use when the keyword is orai, orai token, orai price, orai token price. Dont use it for any other symbol",
        #handle_tool_error=True,
    )
]


def generate_response(query: str):

    llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0.5)
    # llm_chain = LLMChain(llm=llm,prompt=chat_prompt)
    

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True,
        max_iteration=4,
        handle_parsing_errors=True,    
    )

    response = agent.run(
        query
    )

    return str(response)