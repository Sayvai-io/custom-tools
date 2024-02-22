# from narean branch
"""GmailToolkit Template"""
from langchain.agents import (AgentExecutor,create_openai_functions_agent)
# langchain agent main'
from rich import print as rptint 
from langchain_community.agent_toolkits import GmailToolkit
from langchain.chat_models import ChatOpenAI
from langchain import hub


# Create a new LangChain instance
llm = ChatOpenAI(model="gpt-4")

instructions = """You are an assistant who used to help to perform all action related to Gmail."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
rptint(base_prompt)
prompt = base_prompt.partial(instructions=instructions)


class GmailToolkitAgent:

    def __init__(self):
        self.llm = llm
        self.prompt = prompt
        self.tools = None
        self.gmailkit = GmailToolkit()
        
    def initialize_tools(self, tools=None) -> str:
        self.tools = self.gmailkit.get_tools()    
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
        return self.agent_executor.invoke(input={"input": message})["output"]


gmailagent = GmailToolkitAgent()
gmailagent.initialize_tools()
gmailagent.initialize_agent_executor()
print(gmailagent.invoke("Can you create a draft under the subject NEW ONE"))