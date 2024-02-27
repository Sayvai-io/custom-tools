from langchain.tools import BaseTool

from sayvai_tools.tools import load_tools

# pytest for loading tools


def test_load_tools():
    tool = "GetDate"
    ans = load_tools(tool)
    assert isinstance(ans, BaseTool)
    assert ans.__class__.__name__ == tool
    assert ans.__class__.__name__ == "GetDate"
