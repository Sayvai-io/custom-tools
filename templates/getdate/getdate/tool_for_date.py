"""Datetime Template"""

from langchain.agents import AgentExecutor, Tool, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from sayvai_tools.tools.date import GetDate

# Create a new LangChain instance
llm = ChatOpenAI(model="gpt-4")

_SYSTEM_PROMPT: str = (
    """You have access to the GetDate tool, which provides information about the current date and time. 
    Your task is to respond to user queries related to date and time using the current information from the tool. 
    Your responses should be accurate and relevant to the user's query. Use the information from the GetDate tool to provide up-to-date responses."""
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _SYSTEM_PROMPT),
        ("human", "Hello, how are you doing?"),
        ("ai", "I'm doing well, thanks! "),
        ("human", "{input} "),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


class DateTimeAgent:

    def __init__(self):
        self.llm = llm
        self.prompt = prompt
        self.tools = None

    def initialize_tools(self, tools=None) -> str:
        self.tools = tools
        if self.tools is None:
            self.tools = [
                Tool(
                    func=GetDate()._run,
                    name="GetDateTool",
                    description="""A tool that takes no input and returns the current date and time.""",
                ),
            ]
        return "Tools Initialized"

    def initialize_agent_executor(self) -> str:
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            prompt=self.prompt,
            tools=self.tools,  # type: ignore
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,  # type: ignore
            tools=self.tools,  # type: ignore
            verbose=True,
        )
        return "Agent Executor Initialized"

    def invoke(self, message) -> str:
        return self.agent_executor.invoke(input={"input": message})["output"]


dateagent = DateTimeAgent()
dateagent.initialize_tools()
dateagent.initialize_agent_executor()
print(dateagent.invoke("What is the date after 4 days?"))
