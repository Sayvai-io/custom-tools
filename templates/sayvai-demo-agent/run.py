# from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from demoagent.agent import SayvaiDemoAgent
from langchain.llms import OpenAI
from rich import print as rprint

demoag = SayvaiDemoAgent()
demoag.initialize_tools()
rprint(f"[bold green]{demoag.initialize_agent_executor()}[/bold green]")

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        # st_callback = StreamlitCallbackHandler(st.container())
        response = demoag.invoke(prompt)
        st.write(response)