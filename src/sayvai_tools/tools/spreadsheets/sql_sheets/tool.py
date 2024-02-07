from typing import Optional

from langchain.schema import BasePromptTemplate
from langchain.schema.language_model import BaseLanguageModel
from sqlalchemy import create_engine

from sayvai_tools.tools.sql_database.prompt import PROMPT, SQL_PROMPTS
from sayvai_tools.utils.database.dbsheetsbase import SQLDatabaseSheetsBase
from sayvai_tools.utils.database.sheetschain import SheetsDatabaseChain
from sayvai_tools.utils.google.sheets import GSheets


class SQLSheet:
    NotImplementedError


# name = "sqlsheet"
# description = (
#     "Useful for exporting SQL query results to a spreadsheet."
#     "You can use this to generate reports."
# )

# def __init__(self, uri: str, sheet_path: str = "output.xlsx"):
#     self.connection = create_engine(uri).connect()
#     self.sheet_path = sheet_path

# def _run(self, query: str):
#     df = pd.read_sql_query(text(query), self.connection)
#     df.to_excel(self.sheet_path, index=False)
#     return f"Data has been exported to {self.sheet_path}"


class SQLGSheet:
    name = "sqlgsheet"
    description = (
        "Useful for exporting SQL query results to a G-Sheets."
        "You can use this to generate reports."
    )

    def __init__(
        self,
        uri: str,
        llm: BaseLanguageModel,
        prompt: Optional[BasePromptTemplate] = None,
        verbose: bool = False,
    ):
        self.gs = GSheets()
        self.connection = create_engine(uri).connect()
        self.db = SQLDatabaseSheetsBase(engine=self.connection)
        self.llm = llm
        self.prompt = prompt
        self.verbose = verbose

    @classmethod
    def create(cls,**kwargs) -> "SQLGSheet":
        return cls(uri=kwargs["uri"],
                   llm=kwargs["llm"],
                    prompt=kwargs.get("prompt"),
                    verbose=kwargs.get("verbose", False)
                   )

    # sample input save past 30 days data to google sheet from record table
    # table fetched from sql query

    def _run(self, query: str):
        if self.prompt is not None:
            prompt_to_use = self.prompt
        elif self.db.dialect in SQL_PROMPTS:
            prompt_to_use = SQL_PROMPTS[self.db.dialect]
        else:
            prompt_to_use = PROMPT
        inputs = {
            "input": lambda x: x["question"] + "\nSQLQuery: ",
            "top_k": lambda _: self.k,
            "table_info": lambda x: self.db.get_table_info(
                table_names=x.get("table_names_to_use")
            ),
        }
        if "dialect" in prompt_to_use.input_variables:
            inputs["dialect"] = lambda _: (self.db.dialect, prompt_to_use)

        sql_db_chain = SheetsDatabaseChain.from_llm(
            llm=self.llm, db=self.db, prompt=prompt_to_use, verbose=self.verbose
        )

        return sql_db_chain.run(query)


# chain_ouput : str = self.chain.run(query)
# rprint(f"[bold purple]{chain_ouput}[/bold purple]")
# return "Data has been exported to Google Sheets"


# df = pd.read_sql_query(text(chain_ouput), self.connection)
# data_dict = df.to_dict("split")
# columns = data_dict["columns"]
# result = [columns]  # Start with the header
# result.extend(data_dict["data"])  # Add the data
# self.gs.create_sheet()
# self.gs.update_values(result)
