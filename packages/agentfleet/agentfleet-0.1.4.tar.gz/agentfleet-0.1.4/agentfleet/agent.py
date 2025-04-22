from pydantic import BaseModel
from typing import List, Optional
from langchain_core.language_models import BaseChatModel
from langchain.schema.messages import SystemMessage
from langchain_core.tools.structured import StructuredTool
from langchain_core.tools import BaseTool

class Agent(BaseModel):
    name: str = "Agent"
    llm: BaseChatModel
    sys_prompt: str = "You are a helpful Agent"
    util_tools: Optional[List[BaseTool]] = None
    transfer_tools: Optional[List[BaseTool]] = None
    tools: List = []
    util_tools_map: dict = {}
    transfer_tools_map: dict = {}
    messages: List = []

    def __init__(self, 
                 name: str = "Agent", 
                 llm: BaseChatModel = None, 
                 sys_prompt: str = "You are a helpful Agent", 
                 util_tools: Optional[List[StructuredTool]] = None,
                 transfer_tools: Optional[List[StructuredTool]] = None):
        if llm is None:
            raise ValueError("llm cannot be None")
        util_tools = util_tools or []
        transfer_tools = transfer_tools or []
        super().__init__(name=name, llm=llm, sys_prompt=sys_prompt, util_tools=util_tools, transfer_tools=transfer_tools)  # Call the BaseModel's __init__ to handle data validation
        self.tools = util_tools + transfer_tools
        if self.tools:
            self.llm = self.llm.bind_tools(self.tools)
        self.util_tools_map = {tool.name: tool for tool in self.util_tools}
        self.transfer_tools_map = {tool.name: tool for tool in self.transfer_tools}

    def invoke(self, messages):
        new_agent_name = self.name
        new_agent = False
        self.messages = [SystemMessage(self.sys_prompt)]
        self.messages.extend(messages)
        ai_msg = self.llm.invoke(self.messages)
        self.messages.append(ai_msg) 
  
        # logic:
        # 1. check if the ai_msg has tool_calls
        # 2. if yes, check if the tool_call is in util_tools or transfer_tools, the tool call should be either one transfer_tools, or a list of util_tools
        # 3. if yes, if the tool_call is a list of util tools, invoke the tools one by one, 
        # and append the message to self.messages, and invoke the llm again, return the message
        # 4. if the tool_call is a transfer tool, invoke the tool and get the new agent name, 
        # and set new_agent to True 
        
        if ai_msg.tool_calls:
            processed_transfer = False
            processed_util = False
            # Check if there's a transfer tool call first
            for tool_call in ai_msg.tool_calls:
                tool_name = tool_call["name"].lower()
                if tool_name in self.transfer_tools_map:
                    selected_tool = self.transfer_tools_map[tool_name]
                    tool_call["args"] = {}
                    tool_msg = selected_tool.invoke(tool_call)
                    self.messages.append(tool_msg)
                    new_agent_name = tool_msg.content
                    new_agent = True
                    processed_transfer = True
                    break # Process only one transfer tool as per logic

            # If no transfer tool was processed, process util tools
            if not processed_transfer:
                util_tool_msgs = []
                for tool_call in ai_msg.tool_calls:
                    tool_name = tool_call["name"].lower()
                    if tool_name in self.util_tools_map:
                        selected_tool = self.util_tools_map[tool_name]
                        tool_msg = selected_tool.invoke(tool_call)
                        util_tool_msgs.append(tool_msg)
                        processed_util = True
                    # else: handle potential invalid tool calls if necessary
                
                if processed_util:
                    self.messages.extend(util_tool_msgs)
                    # Invoke LLM again after processing util tools
                    ai_msg = self.llm.invoke(self.messages)
                    self.messages.append(ai_msg)
                    # Note: We are not handling tool calls that might arise from this *second* LLM call to avoid loops.

        return self.messages[1:], new_agent_name, new_agent # don't return the system message