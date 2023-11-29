"""Google Forms"""
from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from typing import Any, Optional, List, Text
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


class GForms:
    """Google Forms"""
    def __init__(self, formTitle: str = "Test Form"):
        store = file.Storage('token.json')
        creds = None
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
            creds = tools.run_flow(flow, store)

        self.form_service = discovery.build('forms', 'v1', http=creds.authorize(
            Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)
        
        self.formTitle = formTitle
        self.formID = self.create_form(title=formTitle)
        self.__update_form()
        pass
    
    def create_form(self, title: str = "Test Form"):
        NEW_FORM = {
            "info": {
                "title": title,
            },
        }
        result = self.form_service.forms().create(body=NEW_FORM).execute()
        return result["formId"]
    
    def __update_form(self):
        UPDATE_FORM = {
            "requests": [
                {
                    "updateFormInfo": {
                        "info": {
                            "title": self.formTitle,
                            "description": "created by sayvai-io",
                            "documentTitle": "sayvai-io",
                        },
                        "updateMask": "*",
                    }
                }
            ]
        }
        self.form_service.forms().batchUpdate(formId= self.formID, body=UPDATE_FORM).execute()
    
    def add_question(self, question: str, location : int  = 0) -> str:
        # Creates the initial form
        # Adds the question to the form 
        NEW_QUESTION = {
            "includeFormInResponse": True,
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "itemId": str(location),
                            "title": question,
                            "description": "Please fill in the blank",
                            "questionItem": {
                                "question" : {
                                    "required": True,
                                    "textQuestion": {
                                        "paragraph": False,
                                    }
                                }
                            }
                        },
                        "location": {
                            "index": location,
                        }
                    }
                    
                }
            ]
        }
        self.form_service.forms().batchUpdate(formId=self.formID, body=NEW_QUESTION).execute()
        return "Question has been added"
    
    
    def add_multiple_questions(self, questions: List[str]) -> str:
        for index, question in enumerate(questions):
            self.add_question(question=question, location=index)
        return "All Questions have been added"
    
    

    def get_form(self, form_title: str):
        # Prints the result to show the question has been added
        # get form id from title 
        raise NotImplementedError("This method is not implemented yet")
    
    
    def get_form_url(self, form_title: str):
        raise NotImplementedError("This method is not implemented yet")