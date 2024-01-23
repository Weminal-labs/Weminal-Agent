



from Oraidex_models.config import Config
from Oraidex_models.tool import StockScreenerTool, search_price_orai
from secret import load_secrets

from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType


load_secrets()

tools = [StockScreenerTool(),
    Tool(
        name="search Anything",
        func= SerpAPIWrapper().run,
        description="useful for when you need to answer questions about Document Oraichain Ecosystem.",
    ),
    Tool.from_function(
        func=search_price_orai,
        name="search price orai token",
        description="useful when you need to answer questions about price of only ORAI token. Not any other token on Oraichai",
        handle_tool_error=True,

    )
]



def generate_response(query: str):

    llm = ChatOpenAI(model_name='gpt-3.5-turbo-1106', temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history")
    readonlymemory = ReadOnlySharedMemory(memory=memory)
    
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
        memory=readonlymemory, 
        handle_parsing_errors=True,
        metadata={ "agent_name": "OraidexCrypto" }
    )

    response = agent.run(
        str(query)
    )

    return str(response)