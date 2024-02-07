# DateTime Tools for Langchain Agents 

This is a simple tool to get the current date and time in a specific format.

## Usage

```bash
pip install -r requirements.txt
```

```bash
python getdate.py
```

```python
def invoke(self, message) -> str:
        return self.agent_executor.invoke(input={"input" :message})["output"]
```

```python
dateagent = DateTimeAgent()
dateagent.initialize_tools()
dateagent.initialize_agent_executor()
print(dateagent.invoke("What is the  current date?"))
```