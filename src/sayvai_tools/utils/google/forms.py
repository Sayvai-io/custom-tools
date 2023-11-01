"""Google Forms"""
from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


class GForms:
    """Google Forms"""
    def __init__(self):
        store = file.Storage('token.json')
        creds = None
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
            creds = tools.run_flow(flow, store)

        self.form_service = discovery.build('forms', 'v1', http=creds.authorize(
            Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)
        pass
    
    def create_form(self, title: str):
        NEW_FORM = {
            "info": {
                "title": title,
            }
        }
        result = self.form_service.forms().create(body=NEW_FORM).execute()
        return result["formId"]
    
        # NEW_FORM = {
        # "info": {
        #     "title": "Quickstart form",
        # }
        #  }

        # # Request body to add a multiple-choice question
        # NEW_QUESTION = {
        #     "requests": [{
        #         "createItem": {
        #             "item": {
        #                 "title": "In what year did the United States land a mission on the moon?",
        #                 "questionItem": {
        #                     "question": {
        #                         "required": True,
        #                         "choiceQuestion": {
        #                             "type": "RADIO",
        #                             "options": [
        #                                 {"value": "1965"},
        #                                 {"value": "1967"},
        #                                 {"value": "1969"},
        #                                 {"value": "1971"}
        #                             ],
        #                             "shuffle": True
        #                         }
        #                     }
        #                 },
        #             },
        #             "location": {
        #                 "index": 0
        #             }
        #         }
        #     }]
        # }
    def add_question(self, form_title: str, question: str, options: list) -> str:
        # Creates the initial form
        # Adds the question to the form
        NEW_QUESTION = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": question,
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": option} for option in options
                                    ],
                                    "shuffle": True
                                }
                            }
                        },
                    },
                    "location": {
                        "index": 0
                    }
                }
            }]
        }
        question_setting = self.form_service.forms().batchUpdate(formId=self.create_form(title=form_title), body=NEW_QUESTION).execute()
        return "Question has been added"

    def get_form(self, form_title: str):
        # Prints the result to show the question has been added
        # get form id from title 
        form_id = self.form_service.forms().get(formId=form_title).execute()["formId"]
        get_result = self.form_service.forms().get(formId=form_id).execute()
        print(get_result)
        return get_result