"""Datetime Template"""

from langchain.agents import AgentExecutor, Tool, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from sayvai_tools.tools import GetDate
from sayvai_tools.tools.google_calendar import (AvailableSlotsTool,
                                                CreateEventTool,
                                                DisplayEventsTool,
                                                get_calendar_credentials)

# Create a new LangChain instance
llm = ChatOpenAI(model="gpt-4")

_SYSTEM_PROMPT: str = (
    """
    You have access to two tools: get_date and create_event. 
    - get_date provides information about the current date and time.
    - create_event allows you to create a new event in Google Calendar, with inputs for the start time, end time, and description of the event. The start and end times can be obtained from the get_date tool.

    Use the information from the get_date tool to provide up-to-date responses and the create_event tool to schedule events accurately in Google Calendar. 
    Additionally, you should be able to create events in Google Calendar using the create_event tool based on the user's specified time interval and description.
    """
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
        self.creds = get_calendar_credentials()

    def initialize_tools(self, tools=None) -> str:
        self.tools = tools
        if self.tools is None:
            self.tools = [
                Tool(
                    name="create_event",
                    func=CreateEventTool(credentials=self.creds).run,
                    description="""
                    A tool for creating events with Google Calendar. 
                    It requires the following input parameters in the form of a dictionary:

                    tool_input= {
                        'summary': [A brief description of the event.]
                        'start_time': [The start time of the event on a specific date.]
                        'end_time': [The end time of the event on a specific date.]
                    }

                    Please provide these parameters in the 'tool_input' dictionary.
                    """
                ),
                Tool(
                    func=GetDate()._run,
                    name="get_date",
                    description="""A tool that retrieves the current date and time. 
                   This tool does not require any input parameters.""",
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
print(dateagent.invoke("shedule an appointment tommorrow at 9.30pm for an hour for standup meeting"))
