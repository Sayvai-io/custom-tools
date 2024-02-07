"""Datetime Template"""

from sayvai_tools.tools.date import GetDate
# langchain agent main'
from langchain.tools import BaseTool
from langchain.agents import (
    AgentType,
    AgentExecutor,
    Tool,
    initialize_agent,
    create_openai_functions_agent,
)
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_openai import ChatOpenAI

# Create a new LangChain instance
llm = ChatOpenAI(model="gpt-4")



_SYSTEM_PROMPT : str = """ You are an AI agent, if user asks what is the date 
today invoke GetDateTool .
""" 

prompt = ChatPromptTemplate.from_messages(
[
("system", _SYSTEM_PROMPT ),
("human", "Hello, how are you doing?"),
("ai", "I'm doing well, thanks! "),
("human", "{input} "),
MessagesPlaceholder(variable_name="agent_scratchpad"),
])


class DateTimeAgent:
    
    def __init__(self):
        self.llm = llm
        self.prompt = prompt
        self.tools = None


    def initialize_tools(self, tools = None) -> str:
        self.tools = tools
        if self.tools is None:
            self.tools = [
                Tool(
                func=GetDate()._run,
                name="GetDateTool",
                description="""A tool that returns the current date and time.""",
            ),
            ]
        return "Tools Initialized"
            
    def initialize_agent_executor(self) -> AgentExecutor:
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=self.tools,
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
        )
        return "Agent Executor Initialized"

    def invoke(self, message) -> str:
        return self.agent_executor.invoke(input={"input" :message})["output"]
    
    
dateagent = DateTimeAgent()
dateagent.initialize_tools()
dateagent.initialize_agent_executor()
print(dateagent.invoke("What is the date?"))


