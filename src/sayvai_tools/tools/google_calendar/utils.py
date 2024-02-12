"""Gcalendar tool utils."""
from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, List, Optional, Tuple

if TYPE_CHECKING:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import Resource
    from googleapiclient.discovery import build as build_resource

logger = logging.getLogger(__name__)


def import_google() -> Tuple[Request, Credentials]:
    """Import google libraries.

    Returns:
        Tuple[Request, Credentials]: Request and Credentials classes.
    """
    # google-auth-httplib2
    try:
        from google.auth.transport.requests import Request  # noqa: F401
        from google.oauth2.credentials import Credentials  # noqa: F401
    except ImportError:
        raise ImportError(
            "You need to install google-auth-httplib2 to use this toolkit. "
            "Try running pip install --upgrade google-auth-httplib2"
        )
    return Request, Credentials


def import_installed_app_flow() -> InstalledAppFlow:
    """Import InstalledAppFlow class.

    Returns:
        InstalledAppFlow: InstalledAppFlow class.
    """
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        raise ImportError(
            "You need to install google-auth-oauthlib to use this toolkit. "
            "Try running pip install --upgrade google-auth-oauthlib"
        )
    return InstalledAppFlow


def import_googleapiclient_resource_builder() -> build_resource:
    """Import googleapiclient.discovery.build function.

    Returns:
        build_resource: googleapiclient.discovery.build function.
    """
    try:
        from googleapiclient.discovery import build
    except ImportError:
        raise ImportError(
            "You need to install googleapiclient to use this toolkit. "
            "Try running pip install --upgrade google-api-python-client"
        )
    return build


DEFAULT_SCOPES = ["https://www.googleapis.com/auth/calendar"]
DEFAULT_CREDS_TOKEN_FILE = "token.json"
DEFAULT_CLIENT_SECRETS_FILE = "credentials.json"


def get_calendar_credentials(
        token_file: Optional[str] = None,
        client_secrets_file: Optional[str] = None,
        scopes: Optional[List[str]] = None,
) -> Credentials:
    """Get credentials."""
    Request, Credentials = import_google()
    InstalledAppFlow = import_installed_app_flow()
    creds = None
    scopes = scopes or DEFAULT_SCOPES
    token_file = token_file or DEFAULT_CREDS_TOKEN_FILE
    client_secrets_file = client_secrets_file or DEFAULT_CLIENT_SECRETS_FILE
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes
            )
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return creds


def build_calendar_service(
        credentials: Optional[Credentials] = None,
        service_name: str = "calendar",
        service_version: str = "v3",
) -> Resource:
    """Build a Calendar service."""
    credentials = credentials or get_calendar_credentials()
    builder = import_googleapiclient_resource_builder()
    return builder(service_name, service_version, credentials=credentials)
