"""GmailToolkit Template"""
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_openai_functions_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.agent_toolkits import GmailToolkit
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# langchain agent main'
from sayvai_tools.tools import GetDate
from sayvai_tools.tools.google_calendar import (AvailableSlotsTool,
                                                CreateEventTool,
                                                DisplayEventsTool,
                                                get_calendar_credentials)

# Create a new LangChain instance
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# instructions = """You are an assistant who used to help to perform all action related to Gmail."""
# base_prompt = hub.pull("langchain-ai/openai-functions-template")
# print(base_prompt)
# prompt = base_prompt.partial(instructions=instructions)

_SYSTEM_PROMPT: str = (
    """You are an assistant for SayvAI Software LLP. You are asked to perform based on the user's request.
    You can use following tools to perform the actions:

    <Tools>
    1) GmailCreateDraft - Create a draft email
    2) GmailSendMessage - Send a message
    3) GmailSearch - Search for emails
    4) GmailGetMessage - Get a message 
    5) GmailGetThread - Get a thread
    6) GetDate - Get current date and time (returns only current date and time, utilise current date and time to calculate future or past date and time)
    7) CreateEventTool - to create a new event in Google Calendar(get summary start time and end time from user prompt)
    </Tools>

    Rules:-
    1) To get previous dates and future dates use GetDate tool and calculate the date and time. 
    2) IF user asks about get me tommorow's mail /messages (respond with it is not possible )
    3) if the user asks to do tasks that are related to Gmail,Use the tools and do actions as per reuirements
    4) if the user asks to schedule a meeting, use the CreateEventTool to create a new event in Google Calendar
    5) Agent can aither talk about questions related to Sayvai or utilize the tools to perform actions based on human input 


    """
)

# Your role is an assistant for SayvAI Software LLP. You are asked to perform based on the user's request. You MUST ensure that your answer is unbiased and avoids relying on stereotypes. You can use the following tools to perform the actions: GmailCreateDraft, GmailSendMessage, GmailSearch, GmailGetMessage, GmailGetThread, GetDate. Your task is to use these tools to perform actions as per the user's requirements. You MUST use the same language based on the user's request. Remember to avoid negative language like 'don't'. Agent, Answer a question given in a natural, human-like manner. You will be penalized if you don't. You MUST guide step-by-step thinking. You MUST use output primers. You MUST clearly state the requirements that the model must follow in order to produce content, in the form of keywords, regulations, hints, or instructions. You MUST use leading words like writing 'think step by step'. To inquire about a specific topic or idea and test your understanding, you can use the following phrase: 'Teach me any [theorem/topic/rule name] and include a test at the end, and let me know if my answers are correct after I respond, without providing the answers beforehand.' Your task is to perform actions related to Gmail. Your task is to utilize the tools to perform actions based on human input. Your task is to initiate or continue a text using specific words, phrases, or sentences. I'm providing you with the beginning Gmail tools: <Tools> 1) GmailCreateDraft - Create a draft email 2) GmailSendMessage - Send a message 3) GmailSearch - Search for emails 4) GmailGetMessage - Get a message 5) GmailGetThread - Get a thread 5) GetDate - Get current date and time (returns only current date and time, utilize current date and time to calculate future or past date and time) </Tools> Use the tools to perform actions based on human input. Remember to do actions as per the requirements. Follow the rules to get previous dates and future dates. Use the GetDate tool and calculate the date and time. Remember to use the same language based on the user's request. If the user asks to perform tasks that are related to Gmail, use the tools and do actions as per the requirements. If the user asks for tomorrow's mail/messages, respond with 'It's not possible.'

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _SYSTEM_PROMPT),
        ("human", "{agent_memory} {input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)


class SayvaiDemoAgent:

    def __init__(self):
        self.llm = llm
        self.prompt = prompt
        self.tools = None
        self.memory = ConversationBufferWindowMemory(
            memory_key="agent_memory",
            window_size=10,
        )
        # self.cal_creds = get_calendar_credentials()

    def initialize_tools(self) -> str:
        # self.tools = self.gmailkit.get_tools()
        self.tools = []
        self.tools.append(
            Tool(
                func=GetDate()._run,
                name="GetDateTool",
                description="""A tool that takes no input and returns the current date and time."""
            )
        )
        self.tools.append(
            Tool(
                name="create_event",
                func=CreateEventTool(credentials=get_calendar_credentials())._run,
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
            )
        )
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
            memory=self.memory
        )
        return "Agent Executor Initialized"

    def invoke(self, message) -> str:
        return self.agent_executor.invoke(input={"input": message})["output"]


agent = SayvaiDemoAgent()
agent.initialize_tools()
agent.initialize_agent_executor()

while True:
    agent.invoke(input("Enter your message here"))
