

from langchain.chat_models import ChatOpenAI

from langchain.tools import MoveFileTool, format_tool_to_openai_function
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents import AgentExecutor


from secret import load_secrets
from Contracts.base_input import StockPriceTool, Response, parse
load_secrets()

# tools = [StockPriceTool()]
# functions = [format_tool_to_openai_function(t) for t in tools]



prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Your name is Weminal assistant.\
         Your mission is to help people to generate msg json to swap toke . Only answer you swap success n"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm = ChatOpenAI(temperature=0)
llm_with_tools = llm.bind(
    functions=[
        # The retriever tool
        format_tool_to_openai_function(StockPriceTool()),
        # Response schema
        convert_pydantic_to_openai_function(Response),
    ]
)


agent = (
    {
        "input": lambda x: x["input"],
        # Format agent scratchpad from intermediate steps
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | parse
)


def generate_msg(text: str):
    agent_executor = AgentExecutor(tools=[StockPriceTool()], agent=agent, verbose=True, max_steps=3)
    
    response = agent_executor.invoke(
        {"input": text, "agent_scratchpad": [],},
        return_only_outputs=True,
    )
   

    return response


print(generate_msg("swap 10 orai token to cw20 token"))

# print(answer)
# print(msg)
# print(Response['msg'])

