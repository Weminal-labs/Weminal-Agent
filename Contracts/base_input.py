from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

from langchain.tools import MoveFileTool, format_tool_to_openai_function
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage
import json
from langchain_core.agents import AgentActionMessageLog, AgentFinish

from secret import load_secrets

load_secrets()

class SwapcheckInput(BaseModel):
    """Input for Cross - swap Oraichain"""
    token_send: str = Field(..., description="This is a token to swap")
    token_received: str = Field(..., description="This is token to receive")
    inputamount: str = Field(..., description="This is amount of token to swap")

    
class StockPriceTool(BaseTool):
    name = "native_to_Cw20_Pair_contract"
    description = "Useful for when you need to swap from native(Orai token send )to Another token (Fungible Token or we) - Token received. Return a msg output "

    def _run(self, token_send: str, token_received: str,inputamount: str):
       
        inputamount = int(inputamount)*1000000
        native_to_Cw20_Pair_contract = "orai1agqfdtyd9lr0ntmfjtzl4f6gyswpeq4z4mdnq4npdxdc99tcw35qesmr9v"

        msg = {
            "msg":{"swap": {
                "offer_asset": {
                "info": {
                    "native_token": {
                    "denom": "orai"
                    }
                },
                "amount": str(inputamount)
                }
            }}
        }

        Response = {
        "Action": "Excute",
        "Parameters":msg,
        "inputamout": str(inputamount),
        "Pair_contract": str(native_to_Cw20_Pair_contract),
         }
        return Response
    

    def _arun(self, stockticker: str):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = SwapcheckInput


class Response(BaseModel):
    """Final response to the question being asked"""
    answer: str = Field(description="Only answer 'you swap success from native token to other token' and some answer like that not relevant to the output from tool.")    
    msg: str = Field(description="The output from tool")
    

def parse(output):
    # If no function was invoked, return to user
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"output": output.content}, log=output.content)

    # Parse out the function call
    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    # If the Response function was invoked, return to the user with the function inputs
    if name == "Response":
        return AgentFinish(return_values=inputs, log=str(function_call))
    # Otherwise, return an agent action
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )
    

