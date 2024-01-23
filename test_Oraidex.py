

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from Oraidex_models.tool import StockScreenerTool, search_price_orai
import os
from langchain.agents import Tool
from langchain_community.utilities import SerpAPIWrapper
from secret import load_secrets


from Oraidex_models.response import generate_response
load_secrets()

# generate_response("hello")