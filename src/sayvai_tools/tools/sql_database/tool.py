from sayvai_tools.utils.dbBase import SQLDatabase
from sayvai_tools.utils.dbChain import SQLDatabaseChain
from langchain.tools.base import BaseTool
from typing import Optional
from langchain.schema.language_model import BaseLanguageModel
from sqlalchemy.engine import Engine
from langchain.schema import BasePromptTemplate
from sayvai_tools.tools.sql_database.prompt import PROMPT, SQL_PROMPTS


class Database(BaseTool):
    """Tool that queries vector database."""

    name = "Database"
    description = (
        "Useful for when you need to access menu and order itemns"
            "Input should be a natural language"
    )

    def __init__(self):
        pass

    def sqlchain(
            llm,
            engine: Engine,
            prompt: Optional[BasePromptTemplate] = None,
            verbose: bool = False,
            k: int = 5
    ):
        db=SQLDatabase(engine = engine)

        if prompt is not None:
            prompt_to_use = prompt
        elif db.dialect in SQL_PROMPTS:
            prompt_to_use = SQL_PROMPTS[db.dialect]
        else:
            prompt_to_use = PROMPT
        inputs = {
            "input": lambda x: x["question"] + "\nSQLQuery: ",
            "top_k": lambda _: k,
            "table_info": lambda x: db.get_table_info(
                table_names=x.get("table_names_to_use")
            ),
        }
        if "dialect" in prompt_to_use.input_variables:
            inputs["dialect"] = lambda _: (db.dialect, prompt_to_use)

        sql_db_chain = SQLDatabaseChain.from_llm(
                                                llm=llm,
                                                db=db,
                                                prompt=prompt_to_use,
                                                verbose = verbose
                                                )
        return sql_db_chain

    def _run(
        self,
        query: str
    ) -> str:

        return self.sqlchain.run(query)
    
    async def _arun(self, query: str):

        raise NotImplementedError("SQL database async not implemented")